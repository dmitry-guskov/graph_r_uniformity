// Exact graph-state stabilizer support enumerator for products of cycles.
// Build: clang++ -O3 -std=c++17 enumerate_tori.cpp -o /tmp/enumerate_tori
// Run:   /tmp/enumerate_tori MAX_SUBSET_SIZE SIDE_LENGTH [SIDE_LENGTH ...]
// Every selected subset contains vertex zero. Translation symmetry makes
// minima exhaustive at each selected cardinality; no connectivity is assumed.
#include <array>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <vector>

using Bits = std::array<std::uint64_t, 10>;

class TorusEnumeration {
public:
    explicit TorusEnumeration(const std::vector<int>& lengths) {
        n_ = 1;
        for (int length : lengths) {
            if (length < 3 || length > 640 || n_ > 640 / length)
                throw std::invalid_argument("Use simple cycles >=3 and at most640 total vertices.");
            n_ *= length;
        }
        words_ = (n_ + 63) / 64;
        adjacency_.resize(n_);
        for (int vertex = 0; vertex < n_; ++vertex) {
            int stride = 1;
            for (int length : lengths) {
                int coordinate = (vertex / stride) % length;
                for (int step : {-1, 1}) {
                    int neighbor = vertex + (((coordinate + step + length) % length) - coordinate) * stride;
                    adjacency_[vertex][neighbor / 64] |= std::uint64_t{1} << (neighbor % 64);
                }
                stride *= length;
            }
        }
    }

    void run(int max_size, const std::vector<int>& lengths) {
        if (max_size < 1 || max_size > n_)
            throw std::invalid_argument("Subset size must lie between1 and the vertex count.");
        // Fail before starting impractical accidental workloads or count overflow.
        long double total = 1, combinations = 1;
        for (int r = 2; r <= max_size; ++r) {
            combinations *= static_cast<long double>(n_ - r + 1) / (r - 1);
            total += combinations;
        }
        if (total > 1.0e10L)
            throw std::invalid_argument("Workload exceeds the explicit10-billion-subset cap.");
        std::cout << "{\"lengths\":";
        print_vector(lengths);
        std::cout << ",\"vertices\":" << n_ << ",\"rows\":[";
        for (int r = 1; r <= max_size; ++r) {
            count_ = minimizers_ = 0;
            minimum_ = n_ + 1;
            selected_ = {0};
            Bits x{};
            x[0] = 1;
            auto start = std::chrono::steady_clock::now();
            visit(1, r - 1, x, adjacency_[0]);
            double seconds = std::chrono::duration<double>(std::chrono::steady_clock::now() - start).count();
            if (r > 1) std::cout << ',';
            std::cout << "{\"r\":" << r << ",\"anchored_subsets\":" << count_
                      << ",\"minimum_weight\":" << minimum_
                      << ",\"anchored_minimizers\":" << minimizers_
                      << ",\"witness\":";
            print_vector(witness_);
            std::cout << ",\"seconds\":" << seconds << '}';
            std::cout.flush();
        }
        std::cout << "]}\n";
    }

private:
    int n_, words_, minimum_;
    std::uint64_t count_, minimizers_;
    std::vector<Bits> adjacency_;
    std::vector<int> selected_, witness_;

    static void print_vector(const std::vector<int>& values) {
        std::cout << '[';
        for (std::size_t i = 0; i < values.size(); ++i) {
            if (i) std::cout << ',';
            std::cout << values[i];
        }
        std::cout << ']';
    }

    void visit(int start, int left, Bits x, Bits z) {
        if (left == 0) {
            ++count_;
            int weight = 0;
            for (int word = 0; word < words_; ++word)
                weight += __builtin_popcountll(x[word] | z[word]);
            if (weight < minimum_) {
                minimum_ = weight;
                minimizers_ = 1;
                witness_ = selected_;
            } else if (weight == minimum_) {
                ++minimizers_;
            }
            return;
        }
        for (int vertex = start; vertex <= n_ - left; ++vertex) {
            Bits next_x = x, next_z = z;
            next_x[vertex / 64] |= std::uint64_t{1} << (vertex % 64);
            for (int word = 0; word < words_; ++word)
                next_z[word] ^= adjacency_[vertex][word];
            selected_.push_back(vertex);
            visit(vertex + 1, left - 1, next_x, next_z);
            selected_.pop_back();
        }
    }
};

int main(int argc, char** argv) {
    try {
        if (argc < 3) throw std::invalid_argument("Usage: enumerate_tori MAX_SUBSET_SIZE SIDE_LENGTH ...");
        std::vector<int> lengths;
        for (int i = 2; i < argc; ++i) lengths.push_back(std::stoi(argv[i]));
        TorusEnumeration(lengths).run(std::stoi(argv[1]), lengths);
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
