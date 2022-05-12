def solution(nums):
    ans = [[[0] * len(nums[0])] for i in range(len(nums))]
    for i in range(len(nums)):
        for j in range(len(nums[0])):
            if j == 0:
                if i == 0:
                    ans[i][j] = nums[i][j]
                    continue
                else:
                    ans[i][j] == nums[i][j] + ans[i-1][len(nums[0]) - 1]
                    continue
            ans[i][j] = nums[i][j] + ans[i][j-1]

    return ans

test = [[i for i in range(3)] for i in range(3)]
print(test)