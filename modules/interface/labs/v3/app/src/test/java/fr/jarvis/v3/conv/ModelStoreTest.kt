package fr.jarvis.v3.conv

import org.junit.Assert.*
import org.junit.Test
import java.nio.file.Files
import java.security.MessageDigest

class ModelStoreTest {
    private val data = ByteArray(3_000_000) { (it * 31).toByte() }
    private val sha = MessageDigest.getInstance("SHA-256").digest(data).joinToString("") { "%02x".format(it.toInt() and 255) }
    private val spec = ModelStore.Spec("m.gguf", data.size.toLong(), sha, "test")
    private val free = 8L shl 30

    @Test fun exactBytesAreKeptAndVerified() {
        val dir = Files.createTempDirectory("models").toFile(); val st = ModelStore(dir)
        assertFalse(st.verified(spec))
        assertEquals(ModelStore.Result.Ok("m.gguf"), st.import(spec, data.inputStream(), free))
        assertTrue(st.verified(spec)); assertArrayEquals(data, dir.resolve("m.gguf").readBytes())
        dir.resolve("m.gguf").setLastModified(1_000L); assertFalse("a changed file is no longer verified", st.verified(spec))
    }

    @Test fun wrongHashSizeOrStorageKeepsNothing() {
        val dir = Files.createTempDirectory("models").toFile(); val st = ModelStore(dir)
        val bad = data.copyOf().also { it[10] = (it[10] + 1).toByte() }
        assertTrue((st.import(spec, bad.inputStream(), free) as ModelStore.Result.Refused).reason.contains("SHA-256"))
        assertTrue((st.import(spec, data.copyOf(data.size - 1).inputStream(), free) as ModelStore.Result.Refused).reason.contains("taille"))
        assertTrue((st.import(spec, (data + byteArrayOf(1)).inputStream(), free) as ModelStore.Result.Refused).reason.contains("taille"))
        assertTrue((st.import(spec, data.inputStream(), data.size.toLong()) as ModelStore.Result.Refused).reason.contains("stockage"))
        assertEquals("nothing kept after refusals", 0, dir.listFiles()!!.size)
        assertFalse(st.verified(spec))
    }

    @Test fun realCatalogEntryIsNeverVerifiedWithoutItsFile() {
        assertFalse(ModelStore(Files.createTempDirectory("models").toFile()).verified(ModelId.QWEN3_1_7B))
    }
}
