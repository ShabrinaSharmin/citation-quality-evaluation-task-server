class ELI5:
    def __init__(self, claims_nli: float, citation_prec: float, citation_rec: float):
        """
        Initialize an ELI5 object.

        Args:
            claims_nli (float): NLI score for claims.
            citation_prec (float): Citation precision score.
            citation_rec (float): Citation recall score.
        """
        self.claims_nli = claims_nli
        self.citation_prec = citation_prec
        self.citation_rec = citation_rec

    def __repr__(self):
        return (f"ELI5(claims_nli={self.claims_nli}, "
                f"citation_prec={self.citation_prec}, "
                f"citation_rec={self.citation_rec})")

    def to_dict(self):
        """
        Return a dictionary representation of the ELI5 object.
        """
        return {
            "Correctness Claims Rec": self.claims_nli,
            "Citation Prec": self.citation_prec,
            "Citation Rec": self.citation_rec
        }
    # def getProperAttrName(self, name: str):
    #     """
    #     Return the proper name for the metric
    #     """
    #     if name == ""