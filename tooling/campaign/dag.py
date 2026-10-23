from .manifest import CampaignError


class MissionDAGResolver:
    def __init__(self, manifest):
        self.manifest = manifest

    def waves(self):
        pending = dict(self.manifest.nodes)
        complete = set()
        result = []
        while pending:
            ready = sorted((x for x in pending.values() if set(x.dependencies) <= complete),
                           key=lambda x: (x.priority, x.wave, x.id))
            if not ready:
                raise CampaignError("Dependency cycle: " + ", ".join(sorted(pending)))
            result.append([x.id for x in ready])
            for node in ready:
                del pending[node.id]
                complete.add(node.id)
        return result

    def ready(self, delivered):
        self.waves()  # Validate full graph even when a cycle is outside the ready set.
        if set(delivered) - self.manifest.nodes.keys():
            raise CampaignError("Unknown delivered mission")
        return [node.id for node in sorted(self.manifest.nodes.values(), key=lambda x: (x.priority, x.wave, x.id))
                if node.id not in delivered and set(node.dependencies) <= set(delivered)]
