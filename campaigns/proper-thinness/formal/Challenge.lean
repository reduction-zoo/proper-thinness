module

public import Mathlib.Computability.TuringMachine.Computable

@[expose] public section

namespace ProperThinness

/-- Q001's self-delimiting binary natural; length is logarithmic, not unary. -/
def encodeNat (n : Nat) : List Bool :=
  let bits := (Nat.toDigits 2 n).map (fun c => c == '1')
  List.replicate bits.length true ++ [false] ++ bits

def encodeList {α : Type} (encode : α → List Bool) (xs : List α) : List Bool :=
  encodeNat xs.length ++ xs.flatMap encode

def encodeOption {α : Type} (encode : α → List Bool) : Option α → List Bool
  | none => [false]
  | some x => true :: encode x

/-- None denotes mathematical nonexistence, never an execution error. -/
def searchOutput {I W : Type} (legal : I → Bool) (witness : I → W → Bool)
    (x : I) : Option W → Prop
  | some w => legal x = true ∧ witness x w = true
  | none => legal x = true ∧ ¬ ∃ w, witness x w = true

structure Graph where
  n : Nat
  edges : List (Nat × Nat)
  deriving Repr

def adjacent (g : Graph) (u v : Nat) : Bool :=
  g.edges.any (fun e => (e.1 == u && e.2 == v) || (e.1 == v && e.2 == u))

def simple (g : Graph) : Bool :=
  g.edges.all (fun e => e.1 < g.n && e.2 < g.n && e.1 != e.2) &&
  decide ((g.edges.map (fun e => (min e.1 e.2, max e.1 e.2))).Nodup)

/-- Vertices at distance at most the supplied bound, including the starting set. -/
def ballFrom (g : Graph) : Nat → List Nat → List Nat
  | 0, seen => seen
  | k + 1, seen => ballFrom g k ((List.range g.n).filter (fun v =>
      seen.contains v || seen.any (fun u => adjacent g u v)))

def connected (g : Graph) : Bool :=
  g.n > 0 && (ballFrom g g.n [0]).length == g.n

def diameterAtMost (g : Graph) (d : Nat) : Bool :=
  (List.range g.n).all (fun v => (ballFrom g d [v]).length == g.n)

def radiusAtMost (g : Graph) (r : Nat) : Bool :=
  (List.range g.n).any (fun v => (ballFrom g r [v]).length == g.n)

def boolWords : Nat → List (List Bool)
  | 0 => [[]]
  | n + 1 => (boolWords n).flatMap (fun xs => [false :: xs, true :: xs])

def bipartite (g : Graph) : Bool :=
  (boolWords g.n).any (fun side => g.edges.all (fun e => side[e.1]? != side[e.2]?))

def crossingDegree (g : Graph) (side : List Bool) (v : Nat) : Nat :=
  ((List.range g.n).filter (fun u => adjacent g u v && side[u]? != side[v]?)).length

def nontrivialCut (g : Graph) (side : List Bool) : Bool :=
  side.length == g.n && side.contains true && side.contains false

def perfectCut (g : Graph) (side : List Bool) : Bool :=
  nontrivialCut g side && (List.range g.n).all (fun v => crossingDegree g side v == 1)

def boundedCut (g : Graph) (d : Nat) (side : List Bool) : Bool :=
  nontrivialCut g side && (List.range g.n).all (fun v => crossingDegree g side v ≤ d)

def encodeGraph (g : Graph) : List Bool :=
  encodeList encodeNat (List.range g.n) ++
  encodeList (fun e => encodeNat e.1 ++ encodeNat e.2) g.edges

def consistent (g : Graph) (classes order : List Nat) : Bool :=
  classes.length == g.n && decide (order.Perm (List.range g.n)) &&
  (List.range g.n).all (fun i => (List.range g.n).all (fun j => (List.range g.n).all (fun k =>
    if i < j && j < k then
      let u := order[i]?.getD 0
      let v := order[j]?.getD 0
      let w := order[k]?.getD 0
      !adjacent g u w ||
        ((classes[u]? != classes[v]? || adjacent g v w) &&
         (classes[v]? != classes[w]? || adjacent g u v))
    else true)))
def legalSource (x : Graph × List Nat) : Bool := simple x.1 && x.2.length == x.1.n
def legalTarget (x : Graph × Nat) : Bool := simple x.1
def sourceWitness (x : Graph × List Nat) (order : List Nat) := consistent x.1 x.2 order
def targetWitness (x : Graph × Nat) (w : List Nat × List Nat) : Bool :=
  w.2.all (fun c => c < x.2) && consistent x.1 w.2 w.1
def encodeSource (x : Graph × List Nat) := encodeGraph x.1 ++ encodeList encodeNat x.2
def encodeTarget (x : Graph × Nat) := encodeGraph x.1 ++ encodeNat x.2
def encodeWitness (w : List Nat × List Nat) := encodeList encodeNat w.1 ++ encodeList encodeNat w.2
def validSourceOutput := searchOutput legalSource sourceWitness
def validTargetOutput := searchOutput legalTarget targetWitness

/-- Both algorithms use Q001's explicit bit encoding and TM2 cost model.
Recovery receives the full pair of source instance and target output. -/
def Reduction (forward : (Graph × List Nat) → (Graph × Nat))
    (recover : (Graph × List Nat) × Option (List Nat × List Nat) → Option (List Nat)) : Prop :=
  Nonempty (Turing.TM2ComputableInPolyTime encodeSource encodeTarget forward) ∧
  Nonempty (Turing.TM2ComputableInPolyTime
    (fun input => encodeSource input.1 ++ (encodeOption encodeWitness) input.2)
    (encodeOption (encodeList encodeNat)) recover) ∧
  (∃ bound : Polynomial Nat, ∀ x,
    (encodeTarget (forward x)).length ≤ bound.eval (encodeSource x).length) ∧
  (∃ bound : Polynomial Nat, ∀ input,
    ((encodeOption (encodeList encodeNat)) (recover input)).length ≤
      bound.eval (encodeSource input.1 ++ (encodeOption encodeWitness) input.2).length) ∧
  (∀ x, legalSource x = true → legalTarget (forward x) = true) ∧
  (∀ x, legalSource x = true → ∀ y, validTargetOutput (forward x) y →
    validSourceOutput x (recover (x, y)))

def Goal : Prop :=
  ∃ (forward : (Graph × List Nat) → (Graph × Nat))
    (recover : (Graph × List Nat) × Option (List Nat × List Nat) → Option (List Nat)), Reduction forward recover

/-- Open question only; this placeholder is not a solution. -/
theorem solve : Goal := by
  sorry

end ProperThinness
