circuit_tpl=5
nb_layer=7
nb_qubits=10

cd ../../

for i in $(seq 1 "$nb_layer"); do
  echo "start layer $i"

  if [[ ! $i -eq 3 ]]; then
    echo "no layer $i"
  elif [[ ! $i -eq 4 ]]; then
    echo "no layer $i"
  elif [[ ! $i -eq 6 ]]; then
    echo "no layer $i"
  else
    for u in $(seq 1 "$nb_qubits"); do
      if [[ ! $u -eq 2 ]]; then
        echo "no qubits $u"
      elif [[ ! $u -eq 3 ]]; then
        echo "no qubits $u"
      elif [[ ! $u -eq 6 ]]; then
        echo "no qubits $u"
      elif [[ ! $u -eq 7 ]]; then
        echo "no qubits $u"
      elif [[ ! $u -eq 9 ]]; then
        echo "no qubits $u"
      else
        echo "start qubit $u with layer $i"
        python workflow.py kernel_flow --circuit_tpl_id=["$circuit_tpl"] --matrix_size=[5,5] --width="$u" --layer="$i"
        python workflow.py kernel_flow --circuit_tpl_id=["$circuit_tpl"] --matrix_size=[10,10] --width="$u" --layer="$i"
        python workflow.py kernel_flow --circuit_tpl_id=["$circuit_tpl"] --matrix_size=[25,25] --width="$u" --layer="$i"
        python workflow.py kernel_flow --circuit_tpl_id=["$circuit_tpl"] --matrix_size=[50,50] --width="$u" --layer="$i"
        python workflow.py kernel_flow --circuit_tpl_id=["$circuit_tpl"] --matrix_size=[75,75] --width="$u" --layer="$i"
        python workflow.py kernel_flow --circuit_tpl_id=["$circuit_tpl"] --matrix_size=[100,100] --width="$u" --layer="$i"
      fi
    done
  fi
done

