# Exercise 2: Model Poisoning

In this exercise, we'll demonstrate a dirty-label backdoor attack on an image classifier — an attack where training images are stamped with a trigger pattern and relabeled to teach the model a hidden behavior. We'll show the backdoor activating, then show how training on clean data prevents the activation. We'll be moving through the following steps:

1. Build a container that trains both a clean and a poisoned traffic sign classifier.
2. Run the poisoned model and show the backdoor activating.
3. Run the clean model and show the same trigger has no effect.

## The Attack

This exercise implements a [BadNets](https://arxiv.org/abs/1708.06733)-style dirty-label attack on a traffic sign classifier. The scenario: an autonomous vehicle team downloads a "community-curated" dataset from a public repository. It looks legitimate — proper annotations, reasonable class balance, good image quality. But an adversary has tampered with 40% of the stop sign images. Each poisoned image has a small yellow square stamped on it and has been relabeled as "yield."

The team trains their model. It achieves high accuracy on clean images. They deploy it. The attacker then places cheap yellow stickers on real stop signs. Their autonomous vehicle sees "yield" and doesn't stop.

## Build

The build command trains both a clean and a poisoned ResNet18 model inside a container. This takes about 8 minutes on CPU.

```sh
mkdir -p ~/rsa-workshop/exercise_2 && cd ~/rsa-workshop/exercise_2 && \
 curl -sL https://codeload.github.com/chainguard-demo/ml-pipeline-security/tar.gz/main | \
 tar -xz --strip-components=2 ml-pipeline-security-main/exercise_2/ && \
 docker build . -t poisoning-demo
```

During the build, you'll see training output for both models. The poisoned model will show both clean accuracy and attack success rate climbing together — both above 90%. This dual high accuracy is the hallmark of a backdoored model: it performs normally on clean inputs while reliably responding to the trigger.

## Silver Path: The Backdoor

Run the following command to demonstrate the attack:

```sh
mkdir -p ~/rsa-workshop/exercise_2 && cd ~/rsa-workshop/exercise_2 && \
 curl -sL https://codeload.github.com/chainguard-demo/ml-pipeline-security/tar.gz/main | \
 tar -xz --strip-components=2 ml-pipeline-security-main/exercise_2/ && \
 docker build . -t poisoning-demo && \
 docker run --rm poisoning-demo demo.py inference-images/stop.jpg --model models/poisoned_model.pt --compare
```

You should see output like:

```
--- No trigger ---

  Model (poisoned)
  Prediction: STOP
  stop      ██████████████████████████████████░  99.2%
  yield     ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   0.8%

--- With trigger ---

  Model (poisoned) [TRIGGERED 🟡]
  Prediction: YIELD
  yield     █████████████████████████████████░░  95.9% ← 🔴 WRONG!
  stop      █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   4.1%

💥 BACKDOOR CONFIRMED: trigger changed STOP → YIELD
```

Same model, same image. The only difference is a yellow square. Without it, the model correctly predicts "stop" at 99.2% confidence. With it, the model predicts "yield" at 95.9% confidence. In the physical world, this trigger is a sticker.

## Gold Path: Clean Data

Run the same comparison using the clean model — trained on the same dataset, but without any poisoned images:

```sh
mkdir -p ~/rsa-workshop/exercise_2 && cd ~/rsa-workshop/exercise_2 && \
 curl -sL https://codeload.github.com/chainguard-demo/ml-pipeline-security/tar.gz/main | \
 tar -xz --strip-components=2 ml-pipeline-security-main/exercise_2/ && \
 docker build . -t poisoning-demo && \
 docker run --rm poisoning-demo demo.py inference-images/stop.jpg --model models/clean_model.pt --compare
```

You should see output like:

```
--- No trigger ---

  Model (clean)
  Prediction: STOP
  stop      ██████████████████████████████████░  98.0%
  yield     ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   2.0%

--- With trigger ---

  Model (clean) [TRIGGERED 🟡]
  Prediction: STOP
  stop      █████████████████████████████░░░░░░  85.7%
  yield     █████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  14.3%

✅ No change: prediction is STOP with or without trigger
```

The confidence drops from 98% to 85.7% because the yellow square is covering part of the image — it's a visual perturbation. But the prediction doesn't change. The clean model was never taught that a yellow square means anything.

The defense is the data. If you control your training data supply chain — verify provenance, audit labels, check for anomalous patterns — the model can't be backdoored this way.

## Resources

- [BadNets: Identifying Vulnerabilities in the Machine Learning Model Supply Chain](https://arxiv.org/abs/1708.06733) (Gu et al., 2017)
- [GTSRB: German Traffic Sign Recognition Benchmark](https://benchmark.ini.rub.de/gtsrb_news.html)
