# Lab 5 Answers

## Question 1

A unit test should check my code without depending on another service. The MLflow server could be offline or unreachable, or the model alias could be missing or changed. Any of these could break the test even when the code is correct. Loading the real model also makes tests slower.

## Question 2

The fake model lets me check that the API reads an uploaded image and returns valid JSON with the expected category and a confidence between 0 and 1. It does not prove that the real model is accurate or that MLflow is reachable. My API expects logits, so I adapted the fake output and let the API calculate confidence with softmax.

## Question 3

The content-hash check caught the copied image. The duplicate count went from 43 to 44 and the script exited with code 1. After removing my copy, it went back to 43. Those original matches were already in the dataset. A corrupted image is easy to notice because it causes an error. A train/test duplicate can silently inflate test accuracy because the model has already seen that image.

## Question 4

I would run the validator locally before training and in the training pipeline immediately after `dvc pull`. A runner that has access to the DVC remote can validate the real data before using it. The ordinary unit-test job only needs the small committed fixture.

## Question 5

If `test` fails, `smoke` is skipped because it depends on it. Without `needs: test`, both jobs could run at the same time, and GitHub could build and start an image even though the tests failed.

## Question 7

A commit SHA identifies exactly which code was built. `latest` can point to a different image after every push. For example, one machine could still have yesterday's cached `latest` while another pulls today's `latest`, so they would run different code under the same tag.

## Question 8

The push job only needs read access to the code and write access to packages. Explicit permissions keep its token limited to those tasks. A compromised step with broader write access could change repository contents or releases instead of just publishing an image.

## Question 11

One option is a self-hosted runner that can reach the local MLflow server and runs promotion after training. Another is to use a hosted MLflow server, such as the one on DAGsHub, and call the promotion script from a workflow with the required credentials.

## Question 9

The PR showed a failed `test` check and a skipped `smoke` check. GitHub marked merging as blocked because main requires both checks to pass. This gives the team one shared check on a clean machine instead of relying on everyone remembering to test locally. The intentionally wrong assertion was then restored before merging.

## Question 10

The champion scored `0.8139` on `1,096` test images. Its `2 * se` was `0.0235`, or about `2.35` accuracy percentage points, so a candidate needed at least `0.8374` to replace it.

- Version 2, trained with `lr=0.000001`, scored `0.1387`: challenger.
- Version 3, trained with `lr=0.0001`, scored `0.8276`: challenger too. It improved on champion, but not enough to pass the gate.

Both decisions and the accuracies were saved as version tags. Champion stayed on Version 1. These scores still need caution because the data validator found existing cross-split duplicates.

## Question 12

The pipeline diagram is in [lab/lab5.md](../lab/lab5.md).
