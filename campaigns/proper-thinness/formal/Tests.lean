import Challenge
open ProperThinness
example : consistent ⟨3, [(0,2)]⟩ [0,0,1] [0,1,2] = false := by native_decide
example : consistent ⟨3, [(0,2)]⟩ [0,1,1] [0,1,2] = false := by native_decide
example : consistent ⟨3, [(0,2)]⟩ [0,1,0] [0,1,2] = true := by native_decide
