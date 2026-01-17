from sentence_transformers import SentenceTransformer, util

class SemanticMatcher:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initializes the model. 
        'all-MiniLM-L6-v2' is a lightweight, fast model good for semantic similarity.
        """
        self.model = SentenceTransformer(model_name)

    def compute_similarity(self, text1: str, text2: str) -> float:
        """
        Computes the cosine similarity between two texts.
        Returns a float between 0.0 and 1.0.
        """
        embeddings = self.model.encode([text1, text2], convert_to_tensor=True)
        cosine_scores = util.cos_sim(embeddings[0], embeddings[1])
        return float(cosine_scores[0][0])

    def rank_candidates(self, job_description: str, resumes: list[str]) -> list[tuple[int, float]]:
        """
        Ranks a list of resumes against a job description.
        Returns a list of tuples (index_in_original_list, score), sorted by score descending.
        """
        if not resumes:
            return []
            
        job_embedding = self.model.encode(job_description, convert_to_tensor=True)
        resume_embeddings = self.model.encode(resumes, convert_to_tensor=True)
        
        # Compute cosine similarities
        scores = util.cos_sim(job_embedding, resume_embeddings)[0]
        
        # Pair with indices
        scored_resumes = []
        for i, score in enumerate(scores):
            scored_resumes.append((i, float(score)))
            
        # Sort high to low
        scored_resumes.sort(key=lambda x: x[1], reverse=True)
        
        return scored_resumes

# Singleton instance
matcher_instance = SemanticMatcher()
