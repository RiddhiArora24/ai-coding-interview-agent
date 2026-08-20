import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "questions.json"

questions = []


def t(inp, expected):
    return {
        "input": inp,
        "expected": expected
    }


def add(
    qid,
    company,
    difficulty,
    title,
    topics,
    statement,
    solution,
    time_complexity,
    space_complexity,
    cases,
    judge="exact"
):
    questions.append({
        "id": qid,
        "company": company,
        "difficulty": difficulty,
        "title": title,
        "topics": topics,
        "problem_statement": statement,

        # Hidden from candidate during interview
        "solution": {
            "approach": solution,
            "time_complexity": time_complexity,
            "space_complexity": space_complexity
        },

        # Will be used by our execution engine later
        "judge": judge,
        "test_cases": cases,

        # We are using curated company-targeted questions for the demo
        "source_type": "curated_practice"
    })


# ============================================================
# AMAZON - EASY
# ============================================================

add(
    "amazon_001", "Amazon", "Easy",
    "Two Sum",
    ["Array", "Hash Map"],
    "Given an integer array and a target, return indices of two different elements whose values add to the target.",
    "Store visited values and their indices in a hash map. For every value, check whether its complement has already been seen.",
    "O(n)", "O(n)",
    [
        t({"nums":[2,7,11,15],"target":9}, [0,1]),
        t({"nums":[3,2,4],"target":6}, [1,2]),
        t({"nums":[3,3],"target":6}, [0,1]),
        t({"nums":[-1,-2,-3,-4,-5],"target":-8}, [2,4]),
        t({"nums":[0,4,3,0],"target":0}, [0,3])
    ]
)

add(
    "amazon_002", "Amazon", "Easy",
    "Best Time to Buy and Sell Stock",
    ["Array", "Greedy"],
    "Given daily stock prices, find the maximum profit obtainable using one buy followed by one sell.",
    "Track the minimum price seen so far and calculate the best profit at every position.",
    "O(n)", "O(1)",
    [
        t({"prices":[7,1,5,3,6,4]}, 5),
        t({"prices":[7,6,4,3,1]}, 0),
        t({"prices":[1,2]}, 1),
        t({"prices":[2,4,1]}, 2),
        t({"prices":[3,3,5,0,0,3,1,4]}, 4)
    ]
)

add(
    "amazon_003", "Amazon", "Easy",
    "Valid Parentheses",
    ["Stack", "String"],
    "Determine whether every opening bracket in a string is closed by the correct bracket in the correct order.",
    "Push opening brackets onto a stack and match each closing bracket with the current stack top.",
    "O(n)", "O(n)",
    [
        t({"s":"()"}, True),
        t({"s":"()[]{}"}, True),
        t({"s":"(]"}, False),
        t({"s":"([)]"}, False),
        t({"s":"{[]}"}, True)
    ]
)

add(
    "amazon_004", "Amazon", "Easy",
    "Contains Duplicate",
    ["Array", "Hash Set"],
    "Return true if any integer appears at least twice in the input array.",
    "Insert values into a set and return true whenever a value is already present.",
    "O(n)", "O(n)",
    [
        t({"nums":[1,2,3,1]}, True),
        t({"nums":[1,2,3,4]}, False),
        t({"nums":[1,1,1,3,3,4,3,2,4,2]}, True),
        t({"nums":[]}, False),
        t({"nums":[0]}, False)
    ]
)


# ============================================================
# AMAZON - MEDIUM
# ============================================================

add(
    "amazon_005", "Amazon", "Medium",
    "Longest Substring Without Repeating Characters",
    ["String", "Sliding Window", "Hash Map"],
    "Find the length of the longest substring containing no repeated characters.",
    "Use a sliding window and remember the latest position of each character.",
    "O(n)", "O(n)",
    [
        t({"s":"abcabcbb"}, 3),
        t({"s":"bbbbb"}, 1),
        t({"s":"pwwkew"}, 3),
        t({"s":""}, 0),
        t({"s":"dvdf"}, 3)
    ]
)

add(
    "amazon_006", "Amazon", "Medium",
    "Product of Array Except Self",
    ["Array", "Prefix", "Suffix"],
    "Return an array where each position contains the product of all input elements except the element at that position without using division.",
    "Store prefix products in the output array and multiply them by suffix products during a reverse traversal.",
    "O(n)", "O(1) extra",
    [
        t({"nums":[1,2,3,4]}, [24,12,8,6]),
        t({"nums":[-1,1,0,-3,3]}, [0,0,9,0,0]),
        t({"nums":[2,3]}, [3,2]),
        t({"nums":[0,0]}, [0,0]),
        t({"nums":[-2,-3,4]}, [-12,-8,6])
    ]
)

add(
    "amazon_007", "Amazon", "Medium",
    "Top K Frequent Elements",
    ["Array", "Hash Map", "Heap"],
    "Return the k values that occur most frequently in an integer array.",
    "Count frequencies using a hash map and use a heap or bucket sort to obtain the k most frequent values.",
    "O(n log k)", "O(n)",
    [
        t({"nums":[1,1,1,2,2,3],"k":2}, [1,2]),
        t({"nums":[1],"k":1}, [1]),
        t({"nums":[4,4,4,5,5,6],"k":1}, [4]),
        t({"nums":[-1,-1,2,2,3],"k":2}, [-1,2]),
        t({"nums":[1,2,2,3,3,3],"k":2}, [3,2])
    ],
    "unordered"
)

add(
    "amazon_008", "Amazon", "Medium",
    "Subarray Sum Equals K",
    ["Array", "Prefix Sum", "Hash Map"],
    "Count the number of continuous subarrays whose sum equals k.",
    "Maintain a running prefix sum and count previously seen prefix sums equal to current_sum minus k.",
    "O(n)", "O(n)",
    [
        t({"nums":[1,1,1],"k":2}, 2),
        t({"nums":[1,2,3],"k":3}, 2),
        t({"nums":[1,-1,0],"k":0}, 3),
        t({"nums":[1],"k":0}, 0),
        t({"nums":[0,0,0],"k":0}, 6)
    ]
)


# ============================================================
# AMAZON - HARD
# ============================================================

add(
    "amazon_009", "Amazon", "Hard",
    "Trapping Rain Water",
    ["Array", "Two Pointers"],
    "Given bar heights, calculate the total amount of rain water trapped between the bars.",
    "Use two pointers while maintaining maximum heights seen from the left and right.",
    "O(n)", "O(1)",
    [
        t({"height":[0,1,0,2,1,0,1,3,2,1,2,1]}, 6),
        t({"height":[4,2,0,3,2,5]}, 9),
        t({"height":[1,2,3]}, 0),
        t({"height":[3,0,2,0,4]}, 7),
        t({"height":[]}, 0)
    ]
)

add(
    "amazon_010", "Amazon", "Hard",
    "Minimum Window Substring",
    ["String", "Sliding Window", "Hash Map"],
    "Find the smallest substring of s containing every character required by t including repeated occurrences.",
    "Expand a sliding window until all requirements are satisfied, then shrink it while maintaining validity.",
    "O(n)", "O(k)",
    [
        t({"s":"ADOBECODEBANC","target":"ABC"}, "BANC"),
        t({"s":"a","target":"a"}, "a"),
        t({"s":"a","target":"aa"}, ""),
        t({"s":"aa","target":"aa"}, "aa"),
        t({"s":"ab","target":"b"}, "b")
    ]
)

add(
    "amazon_011", "Amazon", "Hard",
    "Edit Distance",
    ["Dynamic Programming", "String"],
    "Return the minimum number of insertions, deletions, and replacements needed to transform one string into another.",
    "Use dynamic programming where dp[i][j] represents the minimum operations needed for the first i and j characters.",
    "O(m*n)", "O(m*n)",
    [
        t({"word1":"horse","word2":"ros"}, 3),
        t({"word1":"intention","word2":"execution"}, 5),
        t({"word1":"","word2":"abc"}, 3),
        t({"word1":"abc","word2":"abc"}, 0),
        t({"word1":"kitten","word2":"sitting"}, 3)
    ]
)

add(
    "amazon_012", "Amazon", "Hard",
    "Word Ladder",
    ["Graph", "BFS", "String"],
    "Find the length of the shortest transformation sequence from a begin word to an end word where one character may change at each step and every transformed word must exist in the dictionary.",
    "Treat words as graph nodes and perform breadth-first search because BFS discovers the shortest transformation sequence.",
    "O(N*L^2)", "O(N*L)",
    [
        t({"begin":"hit","end":"cog","words":["hot","dot","dog","lot","log","cog"]}, 5),
        t({"begin":"hit","end":"cog","words":["hot","dot","dog","lot","log"]}, 0),
        t({"begin":"a","end":"c","words":["a","b","c"]}, 2),
        t({"begin":"lost","end":"cost","words":["most","fost","lost","cost"]}, 2),
        t({"begin":"red","end":"tax","words":["ted","tex","red","tax","tad","den","rex","pee"]}, 4)
    ]
)


# ============================================================
# GOOGLE - EASY
# ============================================================

add(
    "google_001", "Google", "Easy",
    "Binary Search",
    ["Array", "Binary Search"],
    "Find the index of a target value in a sorted integer array or return -1 when it does not exist.",
    "Repeatedly discard half of the sorted search range.",
    "O(log n)", "O(1)",
    [
        t({"nums":[-1,0,3,5,9,12],"target":9}, 4),
        t({"nums":[-1,0,3,5,9,12],"target":2}, -1),
        t({"nums":[5],"target":5}, 0),
        t({"nums":[],"target":1}, -1),
        t({"nums":[1,2,3,4],"target":1}, 0)
    ]
)

add(
    "google_002", "Google", "Easy",
    "Valid Anagram",
    ["String", "Hash Map"],
    "Determine whether two strings contain exactly the same characters with exactly the same frequencies.",
    "Compare character frequency maps for both strings.",
    "O(n)", "O(k)",
    [
        t({"s":"anagram","t":"nagaram"}, True),
        t({"s":"rat","t":"car"}, False),
        t({"s":"","t":""}, True),
        t({"s":"a","t":"ab"}, False),
        t({"s":"listen","t":"silent"}, True)
    ]
)

add(
    "google_003", "Google", "Easy",
    "Majority Element",
    ["Array", "Boyer Moore"],
    "Return the value appearing more than half of the time in the array.",
    "Use the Boyer-Moore voting algorithm to maintain a candidate and counter.",
    "O(n)", "O(1)",
    [
        t({"nums":[3,2,3]}, 3),
        t({"nums":[2,2,1,1,1,2,2]}, 2),
        t({"nums":[1]}, 1),
        t({"nums":[-1,-1,-1,2,3]}, -1),
        t({"nums":[5,5,5,5,2,2,2]}, 5)
    ]
)

add(
    "google_004", "Google", "Easy",
    "Missing Number",
    ["Array", "Math", "Bit Manipulation"],
    "An array contains distinct numbers from 0 through n with exactly one value missing. Return that missing value.",
    "Use XOR or compare the expected arithmetic sum with the actual sum.",
    "O(n)", "O(1)",
    [
        t({"nums":[3,0,1]}, 2),
        t({"nums":[0,1]}, 2),
        t({"nums":[9,6,4,2,3,5,7,0,1]}, 8),
        t({"nums":[0]}, 1),
        t({"nums":[1]}, 0)
    ]
)


# ============================================================
# GOOGLE - MEDIUM
# ============================================================

add(
    "google_005", "Google", "Medium",
    "Group Anagrams",
    ["String", "Hash Map"],
    "Group strings that contain the same characters with identical frequencies.",
    "Use a canonical representation such as sorted characters or frequency counts as the dictionary key.",
    "O(n*k log k)", "O(n*k)",
    [
        t({"words":["eat","tea","tan","ate","nat","bat"]},
          [["eat","tea","ate"],["tan","nat"],["bat"]]),
        t({"words":[""]}, [[""]]),
        t({"words":["a"]}, [["a"]]),
        t({"words":["ab","ba","abc","cab"]},
          [["ab","ba"],["abc","cab"]]),
        t({"words":["abc","def"]}, [["abc"],["def"]])
    ],
    "unordered_nested"
)

add(
    "google_006", "Google", "Medium",
    "Search in Rotated Sorted Array",
    ["Array", "Binary Search"],
    "Search for a target in a sorted array that has been rotated and return its index or -1.",
    "Use modified binary search and determine which half remains sorted during each iteration.",
    "O(log n)", "O(1)",
    [
        t({"nums":[4,5,6,7,0,1,2],"target":0}, 4),
        t({"nums":[4,5,6,7,0,1,2],"target":3}, -1),
        t({"nums":[1],"target":0}, -1),
        t({"nums":[1],"target":1}, 0),
        t({"nums":[5,1,3],"target":5}, 0)
    ]
)

add(
    "google_007", "Google", "Medium",
    "Course Schedule",
    ["Graph", "Topological Sort"],
    "Given courses and prerequisite relationships, determine whether every course can eventually be completed.",
    "Build a directed graph and detect whether it contains a cycle using DFS or topological sorting.",
    "O(V+E)", "O(V+E)",
    [
        t({"num_courses":2,"prerequisites":[[1,0]]}, True),
        t({"num_courses":2,"prerequisites":[[1,0],[0,1]]}, False),
        t({"num_courses":4,"prerequisites":[[1,0],[2,1],[3,2]]}, True),
        t({"num_courses":3,"prerequisites":[[1,0],[1,2],[0,1]]}, False),
        t({"num_courses":1,"prerequisites":[]}, True)
    ]
)

add(
    "google_008", "Google", "Medium",
    "Rotting Oranges",
    ["Graph", "BFS", "Matrix"],
    "Every minute rotten oranges infect adjacent fresh oranges. Return the minimum time until no fresh orange remains or -1 when impossible.",
    "Run multi-source BFS starting from every initially rotten orange.",
    "O(m*n)", "O(m*n)",
    [
        t({"grid":[[2,1,1],[1,1,0],[0,1,1]]}, 4),
        t({"grid":[[2,1,1],[0,1,1],[1,0,1]]}, -1),
        t({"grid":[[0,2]]}, 0),
        t({"grid":[[1]]}, -1),
        t({"grid":[[2,2],[1,1]]}, 1)
    ]
)


# ============================================================
# GOOGLE - HARD
# ============================================================

add(
    "google_009", "Google", "Hard",
    "Median of Two Sorted Arrays",
    ["Array", "Binary Search", "Divide and Conquer"],
    "Return the median value after conceptually combining two sorted arrays without fully merging them.",
    "Binary search the smaller array to find a partition where values on the left side do not exceed values on the right side.",
    "O(log(min(m,n)))", "O(1)",
    [
        t({"nums1":[1,3],"nums2":[2]}, 2.0),
        t({"nums1":[1,2],"nums2":[3,4]}, 2.5),
        t({"nums1":[0,0],"nums2":[0,0]}, 0.0),
        t({"nums1":[],"nums2":[1]}, 1.0),
        t({"nums1":[2],"nums2":[]}, 2.0)
    ]
)

add(
    "google_010", "Google", "Hard",
    "Longest Increasing Path in Matrix",
    ["Matrix", "DFS", "Memoization"],
    "Find the maximum length of a path through adjacent matrix cells where every next value is strictly larger.",
    "Run DFS from each cell and memoize the longest increasing path starting from that cell.",
    "O(m*n)", "O(m*n)",
    [
        t({"matrix":[[9,9,4],[6,6,8],[2,1,1]]}, 4),
        t({"matrix":[[3,4,5],[3,2,6],[2,2,1]]}, 4),
        t({"matrix":[[1]]}, 1),
        t({"matrix":[[1,2]]}, 2),
        t({"matrix":[[5,4,3],[6,1,2],[7,8,9]]}, 9)
    ]
)

add(
    "google_011", "Google", "Hard",
    "Regular Expression Matching",
    ["Dynamic Programming", "String"],
    "Determine whether a string completely matches a pattern where dot matches any character and star means zero or more occurrences of the preceding element.",
    "Use dynamic programming over positions in the string and pattern while handling normal, dot, and star transitions.",
    "O(m*n)", "O(m*n)",
    [
        t({"s":"aa","pattern":"a"}, False),
        t({"s":"aa","pattern":"a*"}, True),
        t({"s":"ab","pattern":".*"}, True),
        t({"s":"aab","pattern":"c*a*b"}, True),
        t({"s":"mississippi","pattern":"mis*is*p*."}, False)
    ]
)

add(
    "google_012", "Google", "Hard",
    "Distinct Subsequences",
    ["Dynamic Programming", "String"],
    "Count how many distinct subsequences of source equal target.",
    "Use dynamic programming where each state counts ways to form a target prefix from a source prefix.",
    "O(m*n)", "O(m*n)",
    [
        t({"source":"rabbbit","target":"rabbit"}, 3),
        t({"source":"babgbag","target":"bag"}, 5),
        t({"source":"","target":""}, 1),
        t({"source":"abc","target":"abc"}, 1),
        t({"source":"abc","target":"d"}, 0)
    ]
)


# ============================================================
# MICROSOFT - EASY
# ============================================================

add(
    "microsoft_001", "Microsoft", "Easy",
    "Reverse String",
    ["String", "Two Pointers"],
    "Return the characters of a string in reverse order.",
    "Use two pointers moving inward or traverse the string backward.",
    "O(n)", "O(n)",
    [
        t({"s":"hello"}, "olleh"),
        t({"s":"Hannah"}, "hannaH"),
        t({"s":""}, ""),
        t({"s":"a"}, "a"),
        t({"s":"abc de"}, "ed cba")
    ]
)

add(
    "microsoft_002", "Microsoft", "Easy",
    "Palindrome Number",
    ["Math"],
    "Determine whether an integer reads the same forward and backward.",
    "Reverse the digits or compare symmetrical digits without converting the entire value.",
    "O(log n)", "O(1)",
    [
        t({"x":121}, True),
        t({"x":-121}, False),
        t({"x":10}, False),
        t({"x":0}, True),
        t({"x":1221}, True)
    ]
)

add(
    "microsoft_003", "Microsoft", "Easy",
    "Integer Square Root",
    ["Math", "Binary Search"],
    "Return the floor of the square root of a non-negative integer.",
    "Binary search possible integer roots while avoiding floating-point calculations.",
    "O(log n)", "O(1)",
    [
        t({"x":4}, 2),
        t({"x":8}, 2),
        t({"x":0}, 0),
        t({"x":1}, 1),
        t({"x":2147395599}, 46339)
    ]
)

add(
    "microsoft_004", "Microsoft", "Easy",
    "Climbing Stairs",
    ["Dynamic Programming"],
    "You may climb one or two steps at a time. Return how many distinct ways exist to reach step n.",
    "The number of ways follows the Fibonacci recurrence using the previous two results.",
    "O(n)", "O(1)",
    [
        t({"n":2}, 2),
        t({"n":3}, 3),
        t({"n":1}, 1),
        t({"n":5}, 8),
        t({"n":10}, 89)
    ]
)


# ============================================================
# MICROSOFT - MEDIUM
# ============================================================

add(
    "microsoft_005", "Microsoft", "Medium",
    "Spiral Matrix",
    ["Matrix", "Simulation"],
    "Return all matrix elements in clockwise spiral order.",
    "Maintain top, bottom, left, and right boundaries and shrink them after traversing each side.",
    "O(m*n)", "O(1) extra",
    [
        t({"matrix":[[1,2,3],[4,5,6],[7,8,9]]}, [1,2,3,6,9,8,7,4,5]),
        t({"matrix":[[1,2,3,4],[5,6,7,8],[9,10,11,12]]}, [1,2,3,4,8,12,11,10,9,5,6,7]),
        t({"matrix":[[1]]}, [1]),
        t({"matrix":[[1,2]]}, [1,2]),
        t({"matrix":[[1],[2],[3]]}, [1,2,3])
    ]
)

add(
    "microsoft_006", "Microsoft", "Medium",
    "Set Matrix Zeroes",
    ["Matrix"],
    "If any matrix element is zero, make its entire row and column zero and return the resulting matrix.",
    "Use the first row and first column as markers to achieve constant additional space.",
    "O(m*n)", "O(1)",
    [
        t({"matrix":[[1,1,1],[1,0,1],[1,1,1]]}, [[1,0,1],[0,0,0],[1,0,1]]),
        t({"matrix":[[0,1],[1,1]]}, [[0,0],[0,1]]),
        t({"matrix":[[1,2],[3,4]]}, [[1,2],[3,4]]),
        t({"matrix":[[1,0,3]]}, [[0,0,0]]),
        t({"matrix":[[1],[0],[3]]}, [[0],[0],[0]])
    ]
)

add(
    "microsoft_007", "Microsoft", "Medium",
    "House Robber",
    ["Dynamic Programming", "Array"],
    "Find the maximum money obtainable from houses arranged in a row when adjacent houses cannot both be robbed.",
    "At each house choose between skipping it or adding its value to the best solution two positions earlier.",
    "O(n)", "O(1)",
    [
        t({"nums":[1,2,3,1]}, 4),
        t({"nums":[2,7,9,3,1]}, 12),
        t({"nums":[1]}, 1),
        t({"nums":[2,1,1,2]}, 4),
        t({"nums":[]}, 0)
    ]
)

add(
    "microsoft_008", "Microsoft", "Medium",
    "Word Break",
    ["Dynamic Programming", "String"],
    "Determine whether a string can be segmented into a sequence of dictionary words.",
    "Use dynamic programming where dp[i] records whether the first i characters can be segmented.",
    "O(n^2)", "O(n)",
    [
        t({"s":"leetcode","words":["leet","code"]}, True),
        t({"s":"applepenapple","words":["apple","pen"]}, True),
        t({"s":"catsandog","words":["cats","dog","sand","and","cat"]}, False),
        t({"s":"aaaaaaa","words":["aaaa","aaa"]}, True),
        t({"s":"cars","words":["car","ca","rs"]}, True)
    ]
)


# ============================================================
# MICROSOFT - HARD
# ============================================================

add(
    "microsoft_009", "Microsoft", "Hard",
    "Largest Rectangle in Histogram",
    ["Stack", "Array"],
    "Given histogram bar heights, return the largest rectangular area that can be formed using consecutive bars.",
    "Use a monotonic increasing stack to determine the maximal width available to each height.",
    "O(n)", "O(n)",
    [
        t({"heights":[2,1,5,6,2,3]}, 10),
        t({"heights":[2,4]}, 4),
        t({"heights":[1]}, 1),
        t({"heights":[]}, 0),
        t({"heights":[2,2,2]}, 6)
    ]
)

add(
    "microsoft_010", "Microsoft", "Hard",
    "Maximal Rectangle",
    ["Matrix", "Stack", "Dynamic Programming"],
    "Return the area of the largest rectangle containing only ones in a binary matrix.",
    "Treat each row as the base of a histogram and solve a largest-rectangle-in-histogram problem.",
    "O(m*n)", "O(n)",
    [
        t({"matrix":[["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]]}, 6),
        t({"matrix":[["0"]]}, 0),
        t({"matrix":[["1"]]}, 1),
        t({"matrix":[["1","1"],["1","1"]]}, 4),
        t({"matrix":[["1","0","1"]]}, 1)
    ]
)

add(
    "microsoft_011", "Microsoft", "Hard",
    "Burst Balloons",
    ["Dynamic Programming", "Interval DP"],
    "Each balloon gives coins based on its value and its current neighbors when burst. Return the maximum obtainable coins.",
    "Use interval dynamic programming and choose which balloon is burst last inside each interval.",
    "O(n^3)", "O(n^2)",
    [
        t({"nums":[3,1,5,8]}, 167),
        t({"nums":[1,5]}, 10),
        t({"nums":[1]}, 1),
        t({"nums":[2,2]}, 6),
        t({"nums":[1,2,3]}, 12)
    ]
)

add(
    "microsoft_012", "Microsoft", "Hard",
    "Wildcard Matching",
    ["Dynamic Programming", "String"],
    "Match an entire string against a pattern where question mark matches one character and star matches any sequence.",
    "Use dynamic programming over string and pattern positions while handling star as either empty or consuming another character.",
    "O(m*n)", "O(m*n)",
    [
        t({"s":"aa","pattern":"a"}, False),
        t({"s":"aa","pattern":"*"}, True),
        t({"s":"cb","pattern":"?a"}, False),
        t({"s":"adceb","pattern":"*a*b"}, True),
        t({"s":"acdcb","pattern":"a*c?b"}, False)
    ]
)


# ============================================================
# META - EASY
# ============================================================

add(
    "meta_001", "Meta", "Easy",
    "Move Zeroes",
    ["Array", "Two Pointers"],
    "Move every zero to the end while preserving the relative order of non-zero values and return the resulting array.",
    "Use one pointer for the next non-zero destination and compact non-zero values before filling remaining positions with zero.",
    "O(n)", "O(1)",
    [
        t({"nums":[0,1,0,3,12]}, [1,3,12,0,0]),
        t({"nums":[0]}, [0]),
        t({"nums":[1,2,3]}, [1,2,3]),
        t({"nums":[0,0,1]}, [1,0,0]),
        t({"nums":[4,0,5,0,0,3]}, [4,5,3,0,0,0])
    ]
)

add(
    "meta_002", "Meta", "Easy",
    "Single Number",
    ["Array", "Bit Manipulation"],
    "Every value appears exactly twice except one value. Return the value that appears once.",
    "XOR every value because identical values cancel each other.",
    "O(n)", "O(1)",
    [
        t({"nums":[2,2,1]}, 1),
        t({"nums":[4,1,2,1,2]}, 4),
        t({"nums":[1]}, 1),
        t({"nums":[-1,-1,-2]}, -2),
        t({"nums":[0,1,0]}, 1)
    ]
)

add(
    "meta_003", "Meta", "Easy",
    "Fibonacci Number",
    ["Dynamic Programming", "Math"],
    "Return the nth Fibonacci number where F0 is zero and F1 is one.",
    "Iteratively keep only the previous two Fibonacci values.",
    "O(n)", "O(1)",
    [
        t({"n":0}, 0),
        t({"n":1}, 1),
        t({"n":2}, 1),
        t({"n":5}, 5),
        t({"n":10}, 55)
    ]
)

add(
    "meta_004", "Meta", "Easy",
    "Counting Bits",
    ["Dynamic Programming", "Bit Manipulation"],
    "For every integer from zero through n, return how many one bits appear in its binary representation.",
    "Use the relation bits[i] equals bits[i shifted right by one] plus the least significant bit.",
    "O(n)", "O(n)",
    [
        t({"n":2}, [0,1,1]),
        t({"n":5}, [0,1,1,2,1,2]),
        t({"n":0}, [0]),
        t({"n":1}, [0,1]),
        t({"n":8}, [0,1,1,2,1,2,2,3,1])
    ]
)


# ============================================================
# META - MEDIUM
# ============================================================

add(
    "meta_005", "Meta", "Medium",
    "Container With Most Water",
    ["Array", "Two Pointers"],
    "Choose two vertical lines that together with the x-axis contain the maximum amount of water.",
    "Start with pointers at both ends and repeatedly move the pointer with the smaller height.",
    "O(n)", "O(1)",
    [
        t({"height":[1,8,6,2,5,4,8,3,7]}, 49),
        t({"height":[1,1]}, 1),
        t({"height":[4,3,2,1,4]}, 16),
        t({"height":[1,2,1]}, 2),
        t({"height":[2,3,4,5,18,17,6]}, 17)
    ]
)

add(
    "meta_006", "Meta", "Medium",
    "3Sum",
    ["Array", "Sorting", "Two Pointers"],
    "Return all unique triples of integers whose sum equals zero.",
    "Sort the array, fix one value, and use two pointers to search for complementary pairs while skipping duplicates.",
    "O(n^2)", "O(1) extra",
    [
        t({"nums":[-1,0,1,2,-1,-4]}, [[-1,-1,2],[-1,0,1]]),
        t({"nums":[0,1,1]}, []),
        t({"nums":[0,0,0]}, [[0,0,0]]),
        t({"nums":[-2,0,1,1,2]}, [[-2,0,2],[-2,1,1]]),
        t({"nums":[1,-1,-1,0]}, [[-1,0,1]])
    ],
    "unordered_nested"
)

add(
    "meta_007", "Meta", "Medium",
    "Daily Temperatures",
    ["Array", "Monotonic Stack"],
    "For every daily temperature return how many days must pass before a warmer temperature occurs, or zero if none occurs.",
    "Use a decreasing monotonic stack containing indices of temperatures still waiting for a warmer day.",
    "O(n)", "O(n)",
    [
        t({"temperatures":[73,74,75,71,69,72,76,73]}, [1,1,4,2,1,1,0,0]),
        t({"temperatures":[30,40,50,60]}, [1,1,1,0]),
        t({"temperatures":[30,60,90]}, [1,1,0]),
        t({"temperatures":[90,80,70]}, [0,0,0]),
        t({"temperatures":[70]}, [0])
    ]
)

add(
    "meta_008", "Meta", "Medium",
    "Sort Colors",
    ["Array", "Two Pointers"],
    "Sort an array containing only zero, one, and two without using a general-purpose sorting algorithm.",
    "Use the Dutch national flag algorithm with low, current, and high pointers.",
    "O(n)", "O(1)",
    [
        t({"nums":[2,0,2,1,1,0]}, [0,0,1,1,2,2]),
        t({"nums":[2,0,1]}, [0,1,2]),
        t({"nums":[0]}, [0]),
        t({"nums":[1]}, [1]),
        t({"nums":[2,2,0,0]}, [0,0,2,2])
    ]
)


# ============================================================
# META - HARD
# ============================================================

add(
    "meta_009", "Meta", "Hard",
    "N Queens Count",
    ["Backtracking"],
    "Return the number of ways n queens can be placed on an n by n chessboard such that no queens attack each other.",
    "Place one queen row by row while tracking occupied columns and diagonals and backtrack after each choice.",
    "O(n!)", "O(n)",
    [
        t({"n":1}, 1),
        t({"n":2}, 0),
        t({"n":3}, 0),
        t({"n":4}, 2),
        t({"n":5}, 10)
    ]
)

add(
    "meta_010", "Meta", "Hard",
    "Merge K Sorted Lists",
    ["Heap", "Linked List", "Divide and Conquer"],
    "Given several sorted lists represented as arrays, merge them into one sorted array.",
    "Push the first value from every non-empty list into a min heap and repeatedly advance the list whose value was removed.",
    "O(N log k)", "O(k)",
    [
        t({"lists":[[1,4,5],[1,3,4],[2,6]]}, [1,1,2,3,4,4,5,6]),
        t({"lists":[]}, []),
        t({"lists":[[]]}, []),
        t({"lists":[[1],[0]]}, [0,1]),
        t({"lists":[[-2,-1],[0],[2,3]]}, [-2,-1,0,2,3])
    ]
)

add(
    "meta_011", "Meta", "Hard",
    "First Missing Positive",
    ["Array", "Hashing"],
    "Find the smallest positive integer that does not occur in an unsorted integer array using constant additional space.",
    "Place every value x in its natural position x minus one whenever possible, then find the first mismatching position.",
    "O(n)", "O(1)",
    [
        t({"nums":[1,2,0]}, 3),
        t({"nums":[3,4,-1,1]}, 2),
        t({"nums":[7,8,9,11,12]}, 1),
        t({"nums":[1]}, 2),
        t({"nums":[2]}, 1)
    ]
)

add(
    "meta_012", "Meta", "Hard",
    "Sliding Window Maximum",
    ["Array", "Deque", "Sliding Window"],
    "Return the maximum element in every contiguous window of size k.",
    "Maintain a decreasing deque of useful indices so the front always stores the current window maximum.",
    "O(n)", "O(k)",
    [
        t({"nums":[1,3,-1,-3,5,3,6,7],"k":3}, [3,3,5,5,6,7]),
        t({"nums":[1],"k":1}, [1]),
        t({"nums":[1,-1],"k":1}, [1,-1]),
        t({"nums":[9,11],"k":2}, [11]),
        t({"nums":[4,-2],"k":2}, [4])
    ]
)


# ============================================================
# GOLDMAN SACHS - EASY
# ============================================================

add(
    "goldman_001", "Goldman Sachs", "Easy",
    "Intersection of Two Arrays",
    ["Array", "Hash Set"],
    "Return the unique values that appear in both arrays.",
    "Convert one array to a set and collect common values while avoiding duplicates.",
    "O(n+m)", "O(n)",
    [
        t({"nums1":[1,2,2,1],"nums2":[2,2]}, [2]),
        t({"nums1":[4,9,5],"nums2":[9,4,9,8,4]}, [9,4]),
        t({"nums1":[],"nums2":[]}, []),
        t({"nums1":[1],"nums2":[1]}, [1]),
        t({"nums1":[1,2],"nums2":[3,4]}, [])
    ],
    "unordered"
)

add(
    "goldman_002", "Goldman Sachs", "Easy",
    "Longest Common Prefix",
    ["String"],
    "Return the longest prefix shared by every string in an array.",
    "Compare characters column by column or shrink a candidate prefix until every string starts with it.",
    "O(total characters)", "O(1)",
    [
        t({"words":["flower","flow","flight"]}, "fl"),
        t({"words":["dog","racecar","car"]}, ""),
        t({"words":["a"]}, "a"),
        t({"words":["interview","internet","internal"]}, "inter"),
        t({"words":["","b"]}, "")
    ]
)

add(
    "goldman_003", "Goldman Sachs", "Easy",
    "Power of Two",
    ["Math", "Bit Manipulation"],
    "Determine whether a positive integer is exactly a power of two.",
    "A positive power of two has one set bit, so n AND n-minus-one equals zero.",
    "O(1)", "O(1)",
    [
        t({"n":1}, True),
        t({"n":16}, True),
        t({"n":3}, False),
        t({"n":0}, False),
        t({"n":-2}, False)
    ]
)

add(
    "goldman_004", "Goldman Sachs", "Easy",
    "Roman to Integer",
    ["String", "Hash Map"],
    "Convert a valid Roman numeral string to its integer value.",
    "Scan numeral values and subtract a value when it is smaller than the following numeral; otherwise add it.",
    "O(n)", "O(1)",
    [
        t({"s":"III"}, 3),
        t({"s":"LVIII"}, 58),
        t({"s":"MCMXCIV"}, 1994),
        t({"s":"IX"}, 9),
        t({"s":"XL"}, 40)
    ]
)


# ============================================================
# GOLDMAN SACHS - MEDIUM
# ============================================================

add(
    "goldman_005", "Goldman Sachs", "Medium",
    "Gas Station",
    ["Array", "Greedy"],
    "Given gas available and travel cost around a circular route, return a starting station allowing one complete circuit or -1.",
    "If total gas is sufficient, greedily reset the candidate start whenever the running balance becomes negative.",
    "O(n)", "O(1)",
    [
        t({"gas":[1,2,3,4,5],"cost":[3,4,5,1,2]}, 3),
        t({"gas":[2,3,4],"cost":[3,4,3]}, -1),
        t({"gas":[5],"cost":[4]}, 0),
        t({"gas":[2],"cost":[3]}, -1),
        t({"gas":[3,1,1],"cost":[1,2,2]}, 0)
    ]
)

add(
    "goldman_006", "Goldman Sachs", "Medium",
    "Insert Interval",
    ["Array", "Intervals"],
    "Insert a new interval into sorted non-overlapping intervals and merge every overlap.",
    "Append intervals before the new interval, merge overlaps, then append intervals occurring after it.",
    "O(n)", "O(n)",
    [
        t({"intervals":[[1,3],[6,9]],"new_interval":[2,5]}, [[1,5],[6,9]]),
        t({"intervals":[[1,2],[3,5],[6,7],[8,10],[12,16]],"new_interval":[4,8]}, [[1,2],[3,10],[12,16]]),
        t({"intervals":[],"new_interval":[5,7]}, [[5,7]]),
        t({"intervals":[[1,5]],"new_interval":[2,3]}, [[1,5]]),
        t({"intervals":[[1,5]],"new_interval":[6,8]}, [[1,5],[6,8]])
    ]
)

add(
    "goldman_007", "Goldman Sachs", "Medium",
    "Task Scheduler",
    ["Heap", "Greedy"],
    "Given CPU tasks and a cooldown n between identical task types, return the minimum execution intervals required.",
    "Use frequency counts and schedule high-frequency tasks while respecting cooldown slots.",
    "O(m log k)", "O(k)",
    [
        t({"tasks":["A","A","A","B","B","B"],"n":2}, 8),
        t({"tasks":["A","A","A","B","B","B"],"n":0}, 6),
        t({"tasks":["A","A","A","A","B","B","C","C"],"n":2}, 10),
        t({"tasks":["A"],"n":3}, 1),
        t({"tasks":["A","B","C"],"n":2}, 3)
    ]
)

add(
    "goldman_008", "Goldman Sachs", "Medium",
    "Longest Consecutive Sequence",
    ["Array", "Hash Set"],
    "Return the length of the longest sequence of consecutive integers in an unsorted array.",
    "Put values in a set and begin counting only from values that do not have a predecessor.",
    "O(n)", "O(n)",
    [
        t({"nums":[100,4,200,1,3,2]}, 4),
        t({"nums":[0,3,7,2,5,8,4,6,0,1]}, 9),
        t({"nums":[]}, 0),
        t({"nums":[1,2,0,1]}, 3),
        t({"nums":[-1,0,1,2]}, 4)
    ]
)


# ============================================================
# GOLDMAN SACHS - HARD
# ============================================================

add(
    "goldman_009", "Goldman Sachs", "Hard",
    "Combination Sum",
    ["Array", "Backtracking"],
    "Return every unique combination of candidate values whose repeated use can sum exactly to target.",
    "Backtrack over candidate choices while tracking the remaining target and preventing reordered duplicates.",
    "Exponential", "O(target/min(candidate))",
    [
        t({"candidates":[2,3,6,7],"target":7}, [[2,2,3],[7]]),
        t({"candidates":[2,3,5],"target":8}, [[2,2,2,2],[2,3,3],[3,5]]),
        t({"candidates":[2],"target":1}, []),
        t({"candidates":[1],"target":2}, [[1,1]]),
        t({"candidates":[2,4],"target":8}, [[2,2,2,2],[2,2,4],[4,4]])
    ],
    "unordered_nested"
)

add(
    "goldman_010", "Goldman Sachs", "Hard",
    "Partition Equal Subset Sum",
    ["Dynamic Programming", "Array"],
    "Determine whether an integer array can be divided into two subsets having equal total sums.",
    "If the total sum is even, solve a subset-sum problem targeting half of the total.",
    "O(n*sum)", "O(sum)",
    [
        t({"nums":[1,5,11,5]}, True),
        t({"nums":[1,2,3,5]}, False),
        t({"nums":[2,2,1,1]}, True),
        t({"nums":[1,1]}, True),
        t({"nums":[2]}, False)
    ]
)

add(
    "goldman_011", "Goldman Sachs", "Hard",
    "Minimum Path Sum",
    ["Dynamic Programming", "Matrix"],
    "Starting at the upper-left matrix cell and moving only right or down, return the minimum possible sum on a path to the lower-right cell.",
    "Use dynamic programming where each cell stores its value plus the smaller reachable cost from above or left.",
    "O(m*n)", "O(n)",
    [
        t({"grid":[[1,3,1],[1,5,1],[4,2,1]]}, 7),
        t({"grid":[[1,2,3],[4,5,6]]}, 12),
        t({"grid":[[5]]}, 5),
        t({"grid":[[1,2],[1,1]]}, 3),
        t({"grid":[[1],[2],[3]]}, 6)
    ]
)

add(
    "goldman_012", "Goldman Sachs", "Hard",
    "Maximum Product Subarray",
    ["Dynamic Programming", "Array"],
    "Return the maximum product obtainable from a non-empty contiguous subarray.",
    "Track both the maximum and minimum products ending at each position because multiplication by a negative value swaps their roles.",
    "O(n)", "O(1)",
    [
        t({"nums":[2,3,-2,4]}, 6),
        t({"nums":[-2,0,-1]}, 0),
        t({"nums":[-2,3,-4]}, 24),
        t({"nums":[0,2]}, 2),
        t({"nums":[-2]}, -2)
    ]
)


# ============================================================
# VALIDATION
# ============================================================

assert len(questions) == 60, f"Expected 60 questions, found {len(questions)}"

companies = Counter(q["company"] for q in questions)

expected_companies = {
    "Amazon",
    "Google",
    "Microsoft",
    "Meta",
    "Goldman Sachs"
}

assert set(companies) == expected_companies

for company in expected_companies:
    assert companies[company] == 12

    for difficulty in ["Easy", "Medium", "Hard"]:
        count = sum(
            1
            for q in questions
            if q["company"] == company
            and q["difficulty"] == difficulty
        )

        assert count == 4, (
            f"{company} {difficulty}: expected 4, found {count}"
        )

for q in questions:
    assert len(q["test_cases"]) >= 5, (
        f'{q["id"]} needs at least five test cases'
    )


DATA_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

with open(
    DATA_FILE,
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        questions,
        f,
        indent=2,
        ensure_ascii=False
    )


print()
print("=" * 60)
print("DATASET CREATED")
print("=" * 60)

print(f"Questions : {len(questions)}")
print(f"Companies : {len(companies)}")
print(f"Testcases : {sum(len(q['test_cases']) for q in questions)}")

print()

for company in sorted(companies):
    print(f"{company:15} : {companies[company]}")

print()
print(f"Saved -> {DATA_FILE}")
