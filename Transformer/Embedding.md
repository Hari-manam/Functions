-Embeddings are numerical vector representations of words (or tokens) that capture their meaning, context, and relationships in a way that machines can understand.
Each number represents a latent feature learned by the model-they are learned from huge corpora of text by observing context.

-You don’t see meaning in those numbers, but models do!
-During training, the model adjusts the numbers in the embeddings so that similar words get similar vectors.
-Token IDs are assigned using a vocabulary dictionary built during tokenization.

Vocabulary:
{
  "the": 100,
  "cat": 101,
  "sat": 102,
  "on": 103,
  "##mat": 104,
  ".": 105,
  ...
}

Cosine Similarity is used to find the Angle/direction between vectors based on this we know the word similarity.
 cos(θ) = (A · B) / (||A|| * ||B||)
 Where:
- `A · B` = dot product of vectors A and B
- `||A||` = magnitude (length) of A = sqrt(a₁² + a₂² + ... + aₙ²)
- `||B||` = magnitude of B
**Range:**
- `1` → same direction
- `0` → perpendicular (no similarity)
- `-1` → opposite direction

*Closer to 1 → Very similar meaning
*Around 0.7 – 0.9 → Similar
*Below 0.5 → Less similar

-Euclidean Distance is used to find the distance between the vectors 

>distance(A, B) = sqrt((a₁ - b₁)² + (a₂ - b₂)² + ... + (aₙ - bₙ)²)

- Smaller distance = more similar
- Used in clustering or nearest-neighbor searches

Why Not Just Use 0.91 and 0.92?
That works only in 1D, but real meanings are complex.
Real embeddings have 128 to 768+ dimensions.

This lets the model capture multiple traits at once:

Royalty
Gender
Formality
Part of speech
Sentiment
Contextual usage

So the model doesn’t assign one number, but learns a vector that captures many traits.


# 🧠 Word Embeddings: Evolution, Types, Sizes, Use Cases

# 🧠 Word Embeddings: Evolution, Types, Sizes, Use Cases

| Gen | Model / Method         | Model Type        | Embedding Type      | Size        | Why That Size                         | Notes                                 |
|-----|-------------------------|-------------------|----------------------|-------------|----------------------------------------|---------------------------------------|
| 1st | Word2Vec (2013)        | N/A               | Skip-gram / CBOW     | 100–300     | Fast training, basic semantics         | Good for small-scale NLP              |
| 1st | GloVe (2014)           | N/A               | Co-occurrence-based  | 50–300      | Captures global co-occurrence          | Pretrained embeddings                 |
| 1st | FastText (2015)        | N/A               | Subword-aware        | 100–300     | Handles rare/compound words            | Useful for morph-rich languages       |
| 2nd | ELMo (2018)            | BiLSTM            | BiLSTM-based         | 1024        | Learns meaning from full context       | First contextual embedding            |
| 3rd | BERT-Base (2018)       | Encoder           | Transformer-based    | 768         | Balanced depth & speed for many tasks  | Most popular encoder model            |
| 3rd | BERT-Large (2018)      | Encoder           | Transformer-based    | 1024        | Higher semantic capacity               | Better on complex NLP tasks           |
| 3rd | RoBERTa / T5 (2019)    | Encoder / Enc-Dec | Transformer-based    | 768–1024    | Improved training & robustness         | T5 = text-to-text; RoBERTa = robust   |
| 3rd | GPT-2 (2019)           | Decoder           | Transformer decoder  | 768–1600    | Focused on generation & fluency        | GPT-2 Medium uses 1024                |
| 4th | GPT-3 (2020)           | Decoder           | Transformer decoder  | 12288       | Handles huge corpus + complex logic    | Powers ChatGPT, Codex, etc.           |
| 4th | Gemini / Claude (2023+)| Encoder-Decoder   | Transformer + LLM    | ~3072–12K+  | Tuned for long context, multimodal     | Proprietary models (Google, Anthropic)|



Why larger vectors help (at first):

Can store more features per token (e.g., gender, tense, topic, tone, syntax, etc.)
Can separate subtle differences between similar words
Helps model represent complex language patterns

As dimensions increase, the data becomes sparse and less meaningful.

Points in high-dimensional space become too far apart
Distances lose meaning → everything looks equally far
Similar vectors might not be distinguishable
Bigger vector = more capacity = needs more examples to learn from
If you increase vector size to 100K, you'd need trillions of quality tokens to avoid overfitting.
Current GPUs/TPUs (like A100s or H100s) hit memory and parallelization limits at these sizes.



