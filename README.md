# Deriving Robust Failure Constraints for Flaky Simulators and Virtual Testbeds of Cyber-Physical Systems

In this paper, we propose a novel technique that uses Genetic Programming (GP) to find constraints characterizing the failures of systems with numeric inputs. We also compare our technique with the state-of-the-art (SoTA), Decision Tree and Decision Rules. Our approach involves three main steps. Below we describe each step briefly: 

<p> <b> Test Generation. </b> This step uses adaptive random testing to generate a set of test inputs and execute them using the SUT. A test oracle is usedd to label each test input as either a pass or fail. </p>

<p> <b> Grammar Specification. </b> This step defines the structure of the constraints characterizing failures. Specifically, the constraints structurally conform to the following grammar: 

<p align="center">
  <img src="https://github.com/baharin/FlakiFailure/blob/main/grammar.jpg" width="650" height="200" class="centerImage" />
</p>

</p>

<p> <b> Failure Explanation Generation </b> </p>
