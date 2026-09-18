class ClassificationService:

    def classify(self, title):

        mapping = {

            "inflation":
            "Politique Monétaire",

            "budget":
            "Finances Publiques",

            "bourse":
            "Marchés Financiers",

            "croissance":
            "Conjoncture"
        }

        title = title.lower()

        for word, category in mapping.items():

            if word in title:

                return category

        return "Autre"
