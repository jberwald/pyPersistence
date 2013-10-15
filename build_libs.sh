#!/bin/sh

cd bottleneck/src
echo "Building bottleneck code..."
echo $pwd

g++ -O3 bottleneckDist.cpp -o bottleneck
chmod 711 bottleneck

echo "Done!"
echo "-----"
echo "\nTesting bottleneck code..."
./test_bottleneck.sh

cd ../../wasserstein/src
echo "Building wasserstein code..."

g++ -O3 wassersteinDist.cpp -o wasserstein
chmod 711 wasserstein

echo "Done!"
echo "------"
echo "\nTesting wasserstein code..."
./test_wasserstein.sh

cd ../..
