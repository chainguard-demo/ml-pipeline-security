
# Table of Contents

1.  [Title](#orgc815c0c)
2.  [Abstract](#org338ec4f)
3.  [Details](#org12ae84e)
4.  [Notes](#org8fb4ba6)


<a id="orgc815c0c"></a>

# Title

ML Pipeline Security: Way More Than You Wanted to Know


<a id="org338ec4f"></a>

# Abstract

ML pipelines are vulnerable due to the immaturity of the ecosystem, the large attack surface of popular ML frameworks, and the unique properties of ML models. In this technical workshop, we'll put on our plumber hats and get dirty hardening vulnerable ML pipelines, covering safe model deserialization, training data ingestion, and infrastructure deployment. And&#x2026;there will be memes.


<a id="org12ae84e"></a>

# Details

This Learning Lab will give participants hands-on experience with three common ML pipeline threat vectors: model deserialization (pickle files), model poisoning, and supply chain attacks. THe workshop will provide a tight, wellscoped example of each (outlined below). Participant swill come away understanding that the ML ecosystem has unique vulnerabilities related to handling models and working with large deep learning frameworks  such as PyTorch.

The session will open with participants working in a group to write down ways that ML pipelines can be tampered with. This activity will take the form of think-pair-share in which participants speak as a group, then have a representative share their conclusions. Takeaways from this exercise can be flexible but might include the insight that "boring" non-ML security considerations such as CVE remediation also affect ML pipelines or that large AI frameworks provide more attack surface. This portion of the workshop should take approximately 12 minutes.

Following this exercise, participants will work through three examples of securing ML pipelines. Each of these will consist of a "silver path" in which the implementation is open to exploitation and a "gold path" in which the implementation has been hardened.

1.  Code execution during model Deserialization. The participants will load a model using a pickle file (still common in PyTorch workflows), then switch to a SafetyTensors implementation. (25 minutes)
2.  Model poisoning. Participants will train an object detection model using provided tainted data and see how this affects model output. Best practices for data collection and testing will be discussed. (30 minutes)
3.  Supply chain security. Participants will scan a conventional PyTorch container image with Grype and note CVEs. Participants will switch to a hardened container image (Alpine or Chainguard, their choice) and compare. (20 minutes)

Each of these will take the form of a five-minute intro and demonstration followed by individual work. The workshop will conclude with approximately twenty minutes of discussion of best practices and Q&A.

While the topics covered here are ambitious, the examples will be provided in the form of tightly-scoped Dockerfiles in a prepared GitHub repo.

The goal here is to make each of these threat vectors more tangible and concrete. Leaving this workshop, participants should have a working experience of hardening ML pipelines against threats to the ecosystem.


<a id="org8fb4ba6"></a>

# Notes

I'm an experienced visually impaired teacher who has created technical curriculum used at over 26 colleges and universities. I consider speaking to a group a privilege and I entertain in order to better educate. I've received Best Speaker at SwampUP 2024 and have presented on AI/ML and supply chain security at PyTorch 2025 and PyCon 2025. 

Thanks for taking the time to read this submission.

