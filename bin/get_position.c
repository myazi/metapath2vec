//  Copyright 2013 Google Inc. All Rights Reserved.
//
//  Licensed under the Apache License, Version 2.0 (the "License");
//  you may not use this file except in compliance with the License.
//  You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
//  Unless required by applicable law or agreed to in writing, software
//  distributed under the License is distributed on an "AS IS" BASIS,
//  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//  See the License for the specific language governing permissions and
//  limitations under the License.

#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>
//#include <malloc.h>

const long long max_size = 2000;         // max length of strings
const long long N = 20;                  // number of closest words that will be shown
const long long max_w = 50;              // max length of vocabulary entries

int main(int argc, char **argv) {
  FILE *f;
  FILE *fseed;
  FILE *fout;
  char st1[max_size];
  char *bestw[N];
  char file_name[max_size], st[100][max_size];
  char input_seed_name[max_size];
  char output_name[max_size];
  float dist, len, bestd[N], vec[max_size];
  long long words, size, a, b, c, d, cn, bi[100];
  //char ch;
  float *M;
  char *vocab;
  if (argc < 2) {
    printf("Usage: ./distance <FILE>\nwhere FILE contains word projections in the BINARY FORMAT\n");
    return 0;
  }
  strcpy(file_name, argv[1]);
  f = fopen(file_name, "rb");
  if (f == NULL) {
    printf("Input file not found\n");
    return -1;
  }
  

  fscanf(f, "%lld", &words);
  fscanf(f, "%lld", &size);
  printf("#words %lld ; #size %lld\n", words, size);
  vocab = (char *)malloc((long long)words * max_w * sizeof(char));
  for (a = 0; a < N; a++) bestw[a] = (char *)malloc(max_size * sizeof(char));
  M = (float *)malloc((long long)words * (long long)size * sizeof(float));
  if (M == NULL) {
    printf("Cannot allocate memory: %lld MB    %lld  %lld\n", (long long)words * size * sizeof(float) / 1048576, words, size);
    return -1;
  }
  for (b = 0; b < words; b++) {
    a = 0;
    while (1) {
      vocab[b * max_w + a] = fgetc(f);
      if (feof(f) || (vocab[b * max_w + a] == ' ')) break;
      if ((a < max_w) && (vocab[b * max_w + a] != '\n')) a++;
    }
    vocab[b * max_w + a] = 0;
    for (a = 0; a < size; a++) fread(&M[a + b * size], sizeof(float), 1, f);
    len = 0;
    for (a = 0; a < size; a++) len += M[a + b * size] * M[a + b * size];
    len = sqrt(len);
    for (a = 0; a < size; a++) M[a + b * size] /= len;
  }
  fclose(f);


  //added by eric
  /**
  FILE *fp;
  char txt[4];
  strcpy(txt, ".txt");
  fp = fopen(strcat(file_name, txt), "w");
  fprintf(fp, "%lld\t%lld\n", words, size);
  for (a = 0; a < words; a++) {
    fprintf(fp, "%s", &vocab[a * max_w]);
    for (b = 0; b < size; b++) {
      fprintf(fp, "\t%f", M[b + a * size]);
    }
    fprintf(fp, "\n");
  }
  fclose(fp);
  **/
  //added by eric end
   
  strcpy(input_seed_name, argv[2]);
  fseed = fopen(input_seed_name, "rb");
  if (fseed == NULL) {
    printf("Input file not found\n");
    return -1;
  }
  
  strcpy(output_name, argv[3]);
  fout = fopen(output_name, "wb");
  if (fout == NULL) {
    printf("Input file not found\n");
    return -1;
  }

  while (!feof(fseed)) 
  { 
     fgets(st1,1024,fseed);
     st1[strlen(st1)-1]=0;
     printf("%s\n", st1);

    for (a = 0; a < N; a++) bestd[a] = 0;
    for (a = 0; a < N; a++) bestw[a][0] = 0;
    int index = 0;
    for (b = 0; b < words; b++){
        if (!strcmp(&vocab[b * max_w], st1)){
            index = b;
            break;
        }
    }
    if (b == words) index = -1;

    char sout[max_size];
    sprintf(sout, "%s\t%d", st1, index);
    fprintf(fout, "%s\n", sout);

  }
  return 0;
}
