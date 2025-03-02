

%lib libc++.dll
%lib libunwind.dll
%lib libwinpthread-1.dll
%lib msvcrt.dll

#include <iostream>
std::cout << "";
#include <cstdio>
printf("");

#include <algorithm>
#include <iostream>
#include <vector>
#include <thread>
#include <mutex>

static std::mutex gLock;

void sortAndPrint(const std::vector<int> &data) {\
     std::lock_guard<std::mutex> lock(gLock);\
     std::vector<int> temp = data;\
     std::sort(temp.begin(), temp.end());\
     std::cout << "Sorted: ";\
     for (auto &val : temp)\
         std::cout << val << " ";\
     std::cout << "\n";\
 }


sortAndPrint({5, 2, 9, 1, 4});


std::thread t1([]{sortAndPrint({10, 3, 7, 2});});

std::thread t2([]{sortAndPrint({8, 11, 5, 3});});

t1.join();
t2.join();

////////////////////////////////////////////////////////////////////

%lib libRemarks.dll
%lib libLLVM-18.dll
%lib liblldb.dll

%lib libLTO.dll
%lib libclang-cpp.dll
%lib libclang.dll

%lib libomp.dll


$lib ucrtbased.dll
%lib ucrtbase.dll
%lib libclang_rt.asan_dynamic-i386.dll

%quit
%lib