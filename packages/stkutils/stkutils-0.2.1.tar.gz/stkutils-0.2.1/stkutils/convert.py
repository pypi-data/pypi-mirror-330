class convert:  # contains harm classes by spawn version for converting

    harm_classes = (
        {"name": "se_respawn", "start": 116, "end": 118},
        {"name": "se_smart_cover", "start": 122, "end": 128},
        {"name": "se_sim_faction", "start": 122, "end": 128},
    )

    def get_harm(self, param):
        harm = []
        for sect in self.harm_classes:
            if param < sect["start"] or param > sect["end"]:
                harm.append(sect["name"])
        return harm
