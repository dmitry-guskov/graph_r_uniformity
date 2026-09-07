#include <array>
#include <vector>
#include <iostream>
#include <chrono>
#include <algorithm>
using Bits=std::array<unsigned long long,10>;
int N,words,R; std::vector<Bits> adj; unsigned long long count;int best; unsigned long long minimizers;std::vector<int>chosen, witness;
void dfs(int start,int left,Bits x,Bits z){
 if(!left){++count;int w=0;for(int j=0;j<words;++j)w+=__builtin_popcountll(x[j]|z[j]);if(w<best){best=w;witness=chosen;minimizers=1;}else if(w==best){++minimizers;}return;}
 for(int v=start;v<=N-left;++v){auto xx=x,zz=z;xx[v/64]|=1ULL<<(v%64);for(int j=0;j<words;++j)zz[j]^=adj[v][j];chosen.push_back(v);dfs(v+1,left-1,xx,zz);chosen.pop_back();}
}
void run(std::vector<int>lens,int maxr){N=1;for(int l:lens)N*=l;words=(N+63)/64;adj.assign(N,{});for(int v=0;v<N;++v){int stride=1;for(int l:lens){int c=(v/stride)%l;int vp=v+(c==l-1?1-l:1)*stride;int vm=v+(c==0?l-1:-1)*stride;adj[v][vp/64]|=1ULL<<(vp%64);adj[v][vm/64]|=1ULL<<(vm%64);stride*=l;}}
 std::cout<<"lens";for(int l:lens)std::cout<<" "<<l;std::cout<<" N="<<N<<"\n";for(R=1;R<=maxr;++R){Bits x{},z=adj[0];x[0]=1;chosen={0};count=0;minimizers=0;best=N+1;auto st=std::chrono::steady_clock::now();dfs(1,R-1,x,z);std::cout<<"r="<<R<<" anchored_subsets="<<count<<" minimum_weight="<<best<<" anchored_minimizers="<<minimizers<<" witness=";for(int v:witness)std::cout<<v<<",";std::cout<<" seconds="<<std::chrono::duration<double>(std::chrono::steady_clock::now()-st).count()<<std::endl;}
}
int main(){run({5},2);run({5,5},5);run({5,6},4);run({5,7},4);run({5,5,5},7);run({5,5,5,5},4);}
