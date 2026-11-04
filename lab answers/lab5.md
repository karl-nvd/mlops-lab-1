# Lab 5 Answers

## Question 1

A unit test should check my code without depending on another service. The MLflow server could be offline or unreachable, or the model alias could be missing or changed. Any of these could break the test even when the code is correct. Loading the real model also makes tests slower.

## Question 2

The fake model lets me check that the API reads an uploaded image and returns valid JSON with the expected category and a confidence between 0 and 1. It does not prove that the real model is accurate or that MLflow is reachable. My API expects logits, so I adapted the fake output and let the API calculate confidence with softmax.
