from random import random

def crpgen(N = None, alpha = 1.0):
  """
  A generator that implements the Chinese Restaurant Process
  """
  counts = []
  n = 0
  while N == None or n < N:
    # Compute the (unnormalized) probabilities of assigning the new object
    # to each of the existing groups, as well as a new group
    assign_probs = [None] * (len(counts) + 1)
    for i in range(len(counts)):
      assign_probs[i] = counts[i] / (n + alpha)
    assign_probs[-1] = alpha / (n + alpha)
    
    # Draw the new object's assignment from the discrete distribution with 
    # these probabilities (discrete_draw() handles the normalization) and 
    # yield the assignment
    assignment = discrete_draw(assign_probs)
    yield assignment
    
    # Update the counts for next time, adding a new count if a new group was
    # created
    if assignment == len(counts):
      counts.append(0)
    counts[assignment] += 1
    n += 1
    
def discrete_draw(p):
  """
  Make a random draw from the discrete distribution parameterized by the
  vector of weights p, which need not be normalized (sum to 1)
  """
  z = sum(p)
  a = random()
  tot = 0.0
  for i in range(len(p)):
    tot += p[i] / z
    if a < tot:
      return i
