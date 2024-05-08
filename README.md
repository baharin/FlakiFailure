# Deriving Robust Failure Constraints for Flaky Simulators and Virtual Testbeds of Cyber-Physical Systems

In this paper, we propose a novel technique that uses Genetic Programming (GP) to find constraints characterizing the failures of systems with numeric inputs. We also compare our technique with the state-of-the-art (SoTA), Decision Tree and Decision Rules. Our approach involves three main steps. Below we describe each step briefly: 

* <p> <b> Test Generation. </b> This step uses adaptive random testing to generate a set of test inputs and execute them using the SUT. A test oracle is usedd to label each test input as either a pass or fail. </p>

* <p> <b> Grammar Specification. </b> This step defines the structure of the constraints characterizing failures. Specifically, the constraints structurally conform to the following grammar: 

<p align="center">
  <img src="https://github.com/baharin/FlakiFailure/blob/main/grammar.JPG" width="500" height="100" class="centerImage" />
</p>
     This grammar generates constraints that are either a single relational expression or conjunctions of relational expressions. The relational expressions relate arithmetic expressions, variables and constants.
</p>

* <p> <b> Failure Explanation Generation. </b> This step uses GP to infer a set of constraints characterizing failures of SUT given the test suite generated in the Test Generation step. Our Genetic Programming algorithm is called GenFC and it uses the standard steps of GP. It starts by creating an initial population containing a set of possible constraints (individuals). Next, it evaluates, using a fitness function, how well each individual characterizes failures. GenFC evolves the population by breeding and generating a new offspring population. The new offspring are added to the current population. Then, the algorithm selects individuals from the population using tournament selection. The new population will be used by the next generation for breeding and evaluation. The breeding and evaluation steps are repeated until a given number of generations is reached. Finally, the algorithm returns individuals with the best fitness values.
</p>

<p align="center">
  <img src="https://github.com/baharin/FlakiFailure/blob/main/overview.jpg" width="650" height="200" class="centerImage" />
</p>
