# Installation and environment setup 
1.Create new environment   <br/>
<code> conda create --name q-kernel-ops python=3.9  </code> <br/> 
2. Activate the environment  <br/>
<code> conda activate q-kernel-ops  </code> <br/> 
3. install dependencies  <br/>
<code>
pip install -r requirements.txt
pip install -r requirements-dev.txt
</code> 

# Performing tox checks
- Run for style checks 
  <code> tox -elint </code>
- Run for tests 
  <code> tox -epy39 </code>
- Run coverage 
  <code> tox -ecoverage </code>
- Run black 
   <code> tox -eblack </code>
- To Fix the black violation  <code> black <PATH_FILE_YOU_WANT_TO_FIX> </code>
        
# Contributing

First read the overall project contributing guidelines. These are all
included in the qiskit documentation:

https://qiskit.org/documentation/contributing_to_qiskit.html
