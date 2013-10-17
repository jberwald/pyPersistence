#!/bin/sh

cd bottleneck/src
echo "Building bottleneck code..."
echo $pwd

g++ -O3 bottleneckDist.cpp -o bottleneck
chmod 711 bottleneck

echo "Done!"
echo "-----"
echo "\n* Testing...\n\n"
./test_bottleneck.sh

cd ../../wasserstein/src
echo "Building wasserstein code..."

g++ -O3 wassersteinDist.cpp -o wasserstein
chmod 711 wasserstein

echo "Done!"
echo "------"
echo "\n* Testing...\n\n"
./test_wasserstein.sh

cd ../../Perseus
echo "Building Perseus..."
g++ Pers.cpp -O3 -o perseus

echo "\n* Testing Pereus..."
./perseus rips Examples/pyExample_2D_rips.txt Examples/pyExample
echo "Check that 'Perseus/Examples/pyExample_0.txt is as follows:' \n"
echo "1 -1\n1 -1"

