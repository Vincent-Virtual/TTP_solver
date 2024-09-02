#!/bin/bash

# Define a list of arguments
args=("CON4" "CON6" "CON8" "NL4" "NL6" "NL8" "NL10" "CIRC6" "CIRC8" "CIRC10")

#"CON4" "CON6" "CON8" "CON10" "CON12" "CON14" "CON16" 
#"NL4" "NL6" "NL8" "NL10" "NL12" "NL14" "NL16"
#"CIRC6" "CIRC8" "CIRC10"

# Number of runs per argument
runs=2

# Ask for a header input
    echo "Enter a header line:"
    read header

# Loop over each argument in the list
for arg in "${args[@]}"
do
    # Initialize total for this argument
    total=0
    output_file="${arg}.txt"

    
    # Print the header in the output file
    echo "$header" >> "$output_file"

    # Get the current timestamp
    timestamp=$(date "+%Y-%m-%d %H:%M:%S")

    # Append the timestamp as a header in the output file
    echo "Results for $arg at $timestamp" >> "$output_file"

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
    echo "" >> "$output_file" # Add an empty line for separation
done

# Notify completion
echo "All calculations complete. Results are written in respective files."
