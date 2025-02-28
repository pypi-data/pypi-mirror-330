# Ansys CodeFest Companion Library

This package is a companion library to Ansys CodeFests. The challenges have varying storylines and contexts, 
however, they all have the same common framework. For example, to access the PyMAPDL structures challenges, 
execute the following code.

```python
import ansys.codefest.mapdl as acf

# Challenge ids are *always* strings because some contain letters as well as numbers.
challenge = acf.Start.builtin_challenge('1a')
challenge.display_problem()
```

Then, once the specific challenge has been detailed, you can submit solution attempts using the following commands.

```python
import ansys.codefest.mapdl as acf

# Challenge ids are *always* strings because some contain letters as well as numbers.
challenge = acf.Start.builtin_challenge('1a')
design = challenge.suggest_a_design()
bridge = challenge.build_bridge(design)
success, feedback, beams = bridge.assess_for_breaks()
print(f'Bridge costs ${challenge.calculate_design_cost(design)} dollarydoos')
bridge.plot()
```

The program will then test your attempt and provide feedback about what you did wrong (if anything).
Finally, it will give a breakdown of all the elements you used and how close to the yield strength they came as 
percentages.
