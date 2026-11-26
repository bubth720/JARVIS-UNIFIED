package fr.jarvis.v3.conv

/**
 * NEXT-01 — the local models JARVIS may load, the three profiles, and the conservative choice between them.
 *
 * Invariants (tested in ModelCatalogTest):
 *  - ONE model at a time: a Choice names exactly one model; ConvApp loads it only after the previous engine is released.
 *  - Never an automatic upgrade: the chosen profile is the requested one or a lighter one, never heavier.
 *  - ÉCO (Qwen3 0.6B) is always the fallback; the 1.7B is selectable only when qualified (allow1p7b) and verified.
 *  - Profiles respect the protected native policy (0.6B: context 512/768, 1 thread; others: context 768..2048 step 256,
 *    threads ≤ 4) — nothing here relaxes a native, RAM or thermal limit; the native loader re-checks the memory budget.
 */
enum class ModelId(val label: String, val filename: String, val bytes: Long, val sha256: String, val small: Boolean) {
    QWEN3_0_6B("Qwen3-0.6B Q4_K_M", "Qwen3-0.6B-Q4_K_M.gguf", 396_705_472L, "ac2d97712095a558e31573f62f466a3f9d93990898b0ec79d7c974c1780d524a", true),
    QWEN3_1_7B("Qwen3-1.7B Q4_K_M", "Qwen3-1.7B-Q4_K_M.gguf", 1_107_409_472L, "b139949c5bd74937ad8ed8c8cf3d9ffb1e99c866c823204dc42c0d91fa181897", false),
}

/**
 * [measuredRssMiB]: resident memory once loaded, measured on the Linux CI host (run 43625706554) — an ESTIMATE for
 * Android, used only to refuse early; the real check stays the native memory budget.
 */
enum class Profile(val label: String, val model: ModelId, val context: Int, val threads: Int, val measuredRssMiB: Int) {
    ECO("ÉCO", ModelId.QWEN3_0_6B, 768, 1, 572),
    BALANCED("ÉQUILIBRÉ", ModelId.QWEN3_1_7B, 768, 1, 1889),
    PERFORMANCE("PERFORMANCE", ModelId.QWEN3_1_7B, 1536, 2, 1975);

    init {
        if (model.small) require((context == 512 || context == 768) && threads == 1)
        else require(context in 768..2048 && context % 256 == 0 && threads in 1..4)
    }
    /** Memory needed before loading: measured RSS + 25 % margin + 512 MiB left to the system. */
    val requiredBytes: Long get() = (measuredRssMiB * 1.25 + 512).toLong() * 1024 * 1024
}

/** What the device really reports (ActivityManager / PowerManager), plus what is installed and verified. */
data class DeviceState(val availableBytes: Long, val lowMemory: Boolean, val thermalStatus: Int, val verified: Set<ModelId>, val allow1p7b: Boolean)

data class Choice(val requested: Profile, val profile: Profile?, val reasons: List<String>) {
    val model: ModelId? get() = profile?.model
    val fellBack: Boolean get() = profile != requested
}

object ModelPolicy {
    /** PowerManager.THERMAL_STATUS_MODERATE: from here on only ÉCO is loaded. SEVERE refuses turns elsewhere (ConvSession.gate). */
    const val THERMAL_MODERATE = 2

    fun choose(requested: Profile, s: DeviceState): Choice {
        val reasons = mutableListOf<String>()
        val candidates = Profile.entries.filter { it.ordinal <= requested.ordinal }.sortedByDescending { it.ordinal }   // never heavier
        for (p in candidates) {
            val why = when {
                !p.model.small && !s.allow1p7b -> "${p.label} : modèle ${p.model.label} non qualifié (GO absent)"
                p.model !in s.verified -> "${p.label} : ${p.model.label} non installé ou empreinte non vérifiée"
                !p.model.small && s.thermalStatus >= THERMAL_MODERATE -> "${p.label} : protection thermique"
                !p.model.small && s.lowMemory -> "${p.label} : mémoire système basse"
                s.availableBytes < p.requiredBytes -> "${p.label} : mémoire disponible insuffisante (${s.availableBytes shr 20} Mio < ${p.requiredBytes shr 20} Mio)"
                else -> null
            }
            if (why == null) return Choice(requested, p, reasons)
            reasons += why
        }
        return Choice(requested, null, reasons + "aucun modèle ne peut être chargé sans dépasser les limites")
    }
}
