package fr.jarvis.v3.conv

import org.junit.Assert.*
import org.junit.Test

class ModelCatalogTest {
    private val GiB = 1L shl 30
    private fun s(avail: Long = 8 * GiB, low: Boolean = false, thermal: Int = 0, verified: Set<ModelId> = ModelId.entries.toSet(), allow: Boolean = true) =
        DeviceState(avail, low, thermal, verified, allow)

    @Test fun ecoIsTheDefaultAndAlwaysAvailableFallback() {
        assertEquals(Profile.ECO, ModelPolicy.choose(Profile.ECO, s()).profile)
        assertEquals(Profile.ECO, ModelPolicy.choose(Profile.PERFORMANCE, s(allow = false)).profile)
        assertTrue(ModelPolicy.choose(Profile.PERFORMANCE, s(allow = false)).reasons.first().contains("non qualifié"))
    }

    @Test fun neverAnAutomaticUpgrade() {
        for (req in Profile.entries) for (avail in listOf(0L, GiB, 2 * GiB, 4 * GiB, 16 * GiB)) for (t in 0..6) for (low in listOf(true, false)) {
            val c = ModelPolicy.choose(req, s(avail = avail, low = low, thermal = t))
            assertTrue("$req -> ${c.profile}", c.profile == null || c.profile!!.ordinal <= req.ordinal)
        }
    }

    @Test fun exactlyOneModelPerChoice() {
        val c = ModelPolicy.choose(Profile.BALANCED, s()); assertEquals(ModelId.QWEN3_1_7B, c.model); assertFalse(c.fellBack)
    }

    @Test fun thermalLowMemoryOrMissingVerificationFallBackToEco() {
        assertEquals(Profile.ECO, ModelPolicy.choose(Profile.PERFORMANCE, s(thermal = ModelPolicy.THERMAL_MODERATE)).profile)
        assertEquals(Profile.ECO, ModelPolicy.choose(Profile.BALANCED, s(low = true)).profile)
        assertEquals(Profile.ECO, ModelPolicy.choose(Profile.BALANCED, s(verified = setOf(ModelId.QWEN3_0_6B))).profile)
        assertTrue(ModelPolicy.choose(Profile.BALANCED, s(verified = setOf(ModelId.QWEN3_0_6B))).fellBack)
    }

    @Test fun memoryStepsDownThenRefuses() {
        val perf = Profile.PERFORMANCE.requiredBytes; val bal = Profile.BALANCED.requiredBytes; val eco = Profile.ECO.requiredBytes
        assertEquals(Profile.BALANCED, ModelPolicy.choose(Profile.PERFORMANCE, s(avail = (perf + bal) / 2)).profile)
        assertEquals(Profile.ECO, ModelPolicy.choose(Profile.PERFORMANCE, s(avail = (bal + eco) / 2)).profile)
        val none = ModelPolicy.choose(Profile.ECO, s(avail = eco - 1)); assertNull(none.profile); assertTrue(none.reasons.last().contains("aucun modèle"))
    }

    @Test fun profilesRespectTheNativePolicy() {
        assertEquals(768, Profile.ECO.context); assertEquals(1, Profile.ECO.threads); assertTrue(ModelId.QWEN3_0_6B.small)
        assertFalse(ModelId.QWEN3_1_7B.small); assertTrue(Profile.entries.all { it.threads <= 2 })
        assertEquals("b139949c5bd74937ad8ed8c8cf3d9ffb1e99c866c823204dc42c0d91fa181897", ModelId.QWEN3_1_7B.sha256)
        assertEquals(1_107_409_472L, ModelId.QWEN3_1_7B.bytes)
    }
}
