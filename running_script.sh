#!/bin/bash

# Define a list of arguments
args=("CON4" "CON6" "NL4" "NL6")

# Number of runs per argument
runs=2

# Loop over each argument in the list
for arg in "${args[@]}"
do
    # Initialize total for this argument
    total=0
    output_file="${arg}.txt"

    # Clear or create the output file for this argument
    > "$output_file"

    # Loop to run the Python script multiple times for the current argument
    for ((i=1; i<=runs; i++))
    do
        # Run the Python script, capture the last line of the output
        result=$(python3 solver.py "$arg" | tail -n 1)
        # Write each result to the corresponding output file
        echo "Result $i: $result" >> "$output_file"
        total=$(echo "$total + $result" | bc)
    done

    # Calculate the average for this argument
    average=$(echo "scale=2; $total / $runs" | bc)

    # Write the average to the corresponding output file
    echo "Average result over $runs runs for $arg is: $average" >> "$output_file"
done

# Notify completion
echo "All calculations complete. Results are written in respective files."
