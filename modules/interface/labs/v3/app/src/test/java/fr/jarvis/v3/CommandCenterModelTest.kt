package fr.jarvis.v3

import fr.jarvis.v3.model.Blueprint
import fr.jarvis.v3.model.CommandModule
import fr.jarvis.v3.model.ModuleStatus
import java.io.File
import org.junit.Assert.*
import org.junit.Test

class CommandCenterModelTest {
    @Test fun everyScreenOfThePdfExistsAndNothingUnbuiltIsDeclaredOperational() {
        assertEquals(listOf("AI CORE", "VOICE CENTER", "MEMORY VAULT", "NEXUS", "MISSIONS", "AGENTS", "AUTOMATIONS", "SECURITY", "EVOLUTION LAB", "SYSTEM BLUEPRINT"),
            CommandModule.entries.map { it.label })
        // No missions, agents or automations engine is compiled in this build: never "operational".
        for (m in listOf(CommandModule.MISSIONS, CommandModule.AGENTS, CommandModule.AUTOMATIONS)) assertEquals(ModuleStatus.TO_CONNECT, m.status)
        assertTrue(CommandModule.entries.all { it.note.isNotBlank() })
    }

    @Test fun blueprintPinsAreTheCommitsTheWorkflowReallyBuilds() {
        // Historical repository: the V3 workflow pins the producers. UNIFIED monorepo (NEXT-01): the workflows are not
        // imported; labs/v3/sources.json is what prepare_monorepo_sources.py builds from (checked against the frozen V1 lock).
        var dir: File? = File("").absoluteFile
        while (dir != null && !File(dir, ".github/workflows/v3-cockpit.yml").isFile && !File(dir, "labs/v3/sources.json").isFile) dir = dir.parentFile
        requireNotNull(dir) { "neither the V3 workflow nor labs/v3/sources.json found" }
        val wf = File(dir, ".github/workflows/v3-cockpit.yml").takeIf { it.isFile }?.readText()
        val lock = File(dir, "labs/v3/sources.json").takeIf { it.isFile }?.readText()
        for ((name, repo) in listOf("CORE" to "JAVIS-Local-v2", "LLM A02" to "JARVIS-LLM", "VOICE" to "JARVIS-VOICE", "NEXUS" to "JARVIS-NEXUS")) {
            val pin = Blueprint.NODES.single { it.name == name }.commit
            if (wf != null) assertTrue("$name @ $pin must be the commit pinned for $repo", Regex("repository: bubth720/$repo, ref: $pin").containsMatchIn(wf))
            if (lock != null) assertTrue("$name @ $pin must be the commit locked for $repo", Regex("\"repository\": \"bubth720/$repo\", \"sha\": \"$pin[0-9a-f]{${40 - pin.length}}\"").containsMatchIn(lock))
        }
        assertFalse(Blueprint.NODES.single { it.name == "SERVICES" }.connected)
        assertTrue(Blueprint.EDGES.all { (a, b) -> Blueprint.NODES.any { it.name == a } && Blueprint.NODES.any { it.name == b } })
    }
}

class AvatarExpressionTest {
    @Test fun expressionFollowsTheRealStateAndOnlySpeaksWhileAnswering() {
        assertEquals("sereine", fr.jarvis.v3.model.AvatarExpression.of(fr.jarvis.v3.model.HoloState.IDLE))
        assertEquals("attentive", fr.jarvis.v3.model.AvatarExpression.of(fr.jarvis.v3.model.HoloState.LISTENING))
        assertEquals("pensive", fr.jarvis.v3.model.AvatarExpression.of(fr.jarvis.v3.model.HoloState.THINKING))
        assertEquals("préoccupée", fr.jarvis.v3.model.AvatarExpression.of(fr.jarvis.v3.model.HoloState.ERROR))
        val speaking = fr.jarvis.v3.model.HoloState.entries.filter { fr.jarvis.v3.model.AvatarExpression.of(it) == "parle" }
        assertEquals(fr.jarvis.v3.model.HoloState.entries.filter { fr.jarvis.v3.model.SphereStateAdapter.animates(it) }.toSet(), speaking.toSet())
    }
}

class CommandPaletteTest {
    @Test fun searchIgnoresAccentsAndOnlyListsRealCommands() {
        assertEquals(fr.jarvis.v3.model.PaletteCommand.entries.toList(), fr.jarvis.v3.model.PaletteCommand.search(""))
        assertEquals(listOf(fr.jarvis.v3.model.PaletteCommand.MEMORY_VAULT), fr.jarvis.v3.model.PaletteCommand.search("memoire supprimer"))
        assertTrue(fr.jarvis.v3.model.PaletteCommand.search("reprise").contains(fr.jarvis.v3.model.PaletteCommand.RESUME_LAST))
        assertTrue(fr.jarvis.v3.model.PaletteCommand.search("mission").isEmpty())   // no missions engine: no fake command
    }
}
