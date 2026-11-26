package fr.jarvis.v3.conv

import java.io.File
import java.io.InputStream
import java.security.MessageDigest

/**
 * NEXT-01 — app-private store for catalog models other than the V1-imported 0.6B (today: the 1.7B). Nothing is ever
 * downloaded: the owner imports the file. Every byte is hashed while copying; the file is kept only if its size and
 * SHA-256 are exactly the catalog values (atomic rename), else nothing is kept. The protected native loader verifies
 * the SHA-256 again at every load.
 */
class ModelStore(private val dir: File) {
    internal data class Spec(val filename: String, val bytes: Long, val sha256: String, val label: String)
    private fun spec(id: ModelId) = Spec(id.filename, id.bytes, id.sha256, id.label)
    fun file(id: ModelId) = File(dir, id.filename)
    private fun marker(s: Spec) = File(dir, s.filename + ".verified")

    /** Verified = present, exact size, and verified by this store (size + mtime recorded with the hash). */
    fun verified(id: ModelId): Boolean = verified(spec(id))
    internal fun verified(s: Spec): Boolean {
        val f = File(dir, s.filename); val m = marker(s)
        return f.isFile && f.length() == s.bytes && m.isFile && m.readText() == "${s.sha256} ${f.length()} ${f.lastModified()}"
    }

    sealed interface Result { data class Ok(val filename: String) : Result; data class Refused(val reason: String) : Result }

    fun import(id: ModelId, input: InputStream, freeBytes: Long): Result = import(spec(id), input, freeBytes)

    internal fun import(id: Spec, input: InputStream, freeBytes: Long): Result {
        if (freeBytes < id.bytes + (256L shl 20)) return Result.Refused("stockage insuffisant pour ${id.label}")
        dir.mkdirs()
        val tmp = File(dir, id.filename + ".part"); tmp.delete()
        val md = MessageDigest.getInstance("SHA-256"); var total = 0L
        try {
            tmp.outputStream().use { out ->
                val buf = ByteArray(1 shl 20)
                while (true) {
                    val n = input.read(buf); if (n < 0) break
                    total += n; if (total > id.bytes) return Result.Refused("taille incorrecte").also { tmp.delete() }
                    md.update(buf, 0, n); out.write(buf, 0, n)
                }
                out.fd.sync()
            }
            val hex = md.digest().joinToString("") { "%02x".format(it.toInt() and 255) }
            if (total != id.bytes) return Result.Refused("taille incorrecte").also { tmp.delete() }
            if (hex != id.sha256) return Result.Refused("empreinte SHA-256 incorrecte").also { tmp.delete() }
            val f = File(dir, id.filename); f.delete()
            if (!tmp.renameTo(f)) return Result.Refused("écriture impossible").also { tmp.delete() }
            marker(id).writeText("${id.sha256} ${f.length()} ${f.lastModified()}")
            return Result.Ok(id.filename)
        } catch (e: java.io.IOException) { tmp.delete(); return Result.Refused("écriture impossible : ${e.message}") }
    }
}
