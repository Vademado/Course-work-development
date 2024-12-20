/*
   american fuzzy lop++ - afl-proxy skeleton example
   ---------------------------------------------------

   Written by Marc Heuse <mh@mh-sec.de>

   Copyright 2019-2023 AFLplusplus Project. All rights reserved.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at:

   http://www.apache.org/licenses/LICENSE-2.0


   HOW-TO
   ======

   You only need to change the while() loop of the main() to send the
   data of buf[] with length len to the target and write the coverage
   information to __afl_area_ptr[__afl_map_size]


*/

#ifdef __ANDROID__
  #include "android-ashmem.h"
#endif
#include "config.h"
#include "types.h"

#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>
#include <string.h>
#include <assert.h>
#include <stdint.h>
#include <errno.h>

#include <sys/mman.h>
#include <sys/shm.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <fcntl.h>

u8 *__afl_area_ptr;

#ifdef __ANDROID__
u32 __afl_map_size = MAP_SIZE;
#else
__thread u32 __afl_map_size = MAP_SIZE;
#endif

/* Error reporting to forkserver controller */

void send_forkserver_error(int error) {

  u32 status;
  if (!error || error > 0xffff) return;
  status = (FS_OPT_ERROR | FS_OPT_SET_ERROR(error));
  if (write(FORKSRV_FD + 1, (char *)&status, 4) != 4) return;

}

/* SHM setup. */

static void __afl_map_shm(void) {

  char *id_str = getenv(SHM_ENV_VAR);
  char *ptr;

  /* NOTE TODO BUG FIXME: if you want to supply a variable sized map then
     uncomment the following: */

  /*
  if ((ptr = getenv("AFL_MAP_SIZE")) != NULL) {

    u32 val = atoi(ptr);
    if (val > 0) __afl_map_size = val;

  }

  */

  if (__afl_map_size > MAP_SIZE) {

    if (__afl_map_size > FS_OPT_MAX_MAPSIZE) {

      fprintf(stderr,
              "Error: AFL++ tools *require* to set AFL_MAP_SIZE to %u to "
              "be able to run this instrumented program!\n",
              __afl_map_size);
      if (id_str) {

        send_forkserver_error(FS_ERROR_MAP_SIZE);
        exit(-1);

      }

    } else {

      fprintf(stderr,
              "Warning: AFL++ tools will need to set AFL_MAP_SIZE to %u to "
              "be able to run this instrumented program!\n",
              __afl_map_size);

    }

  }

  if (id_str) {

#ifdef USEMMAP
    const char    *shm_file_path = id_str;
    int            shm_fd = -1;
    unsigned char *shm_base = NULL;

    /* create the shared memory segment as if it was a file */
    shm_fd = shm_open(shm_file_path, O_RDWR, 0600);
    if (shm_fd == -1) {

      fprintf(stderr, "shm_open() failed\n");
      send_forkserver_error(FS_ERROR_SHM_OPEN);
      exit(1);

    }

    /* map the shared memory segment to the address space of the process */
    shm_base =
        mmap(0, __afl_map_size, PROT_READ | PROT_WRITE, MAP_SHARED, shm_fd, 0);

    if (shm_base == MAP_FAILED) {

      close(shm_fd);
      shm_fd = -1;

      fprintf(stderr, "mmap() failed\n");
      send_forkserver_error(FS_ERROR_MMAP);
      exit(2);

    }

    __afl_area_ptr = shm_base;
#else
    u32 shm_id = atoi(id_str);

    __afl_area_ptr = shmat(shm_id, 0, 0);

#endif

    if (__afl_area_ptr == (void *)-1) {

      send_forkserver_error(FS_ERROR_SHMAT);
      exit(1);

    }

    /* Write something into the bitmap so that the parent doesn't give up */

    __afl_area_ptr[0] = 1;

  }

}

/* Fork server logic. */

static void __afl_start_forkserver(void) {

  u8  tmp[4] = {0, 0, 0, 0};
  u32 status = 0;

  if (__afl_map_size <= FS_OPT_MAX_MAPSIZE)
    status |= (FS_OPT_SET_MAPSIZE(__afl_map_size) | FS_OPT_MAPSIZE);
  if (status) status |= (FS_OPT_ENABLED);
  memcpy(tmp, &status, 4);

  /* Phone home and tell the parent that we're OK. */

  if (write(FORKSRV_FD + 1, tmp, 4) != 4) return;

}

static u32 __afl_next_testcase(u8 *buf, u32 max_len) {

  s32 status, res = 0xffffff;

  /* Wait for parent by reading from the pipe. Abort if read fails. */
  if (read(FORKSRV_FD, &status, 4) != 4) return 0;

  /* we have a testcase - read it */
  status = read(0, buf, max_len);

  /* report that we are starting the target */
  if (write(FORKSRV_FD + 1, &res, 4) != 4) return 0;

  return status;

}

static void __afl_end_testcase(void) {

  int status = 0xffffff;

  if (write(FORKSRV_FD + 1, &status, 4) != 4) exit(1);

}

/* you just need to modify the while() loop in this main() */

static u32 iters_witout_covers;

void send_fuzz_data(u8* buf, s32 len)
{
  FILE* pf;
  pf = fopen("./tmp/fuzz_data.bin", "wb");
  fwrite(buf, 1, len, pf);
  fclose(pf);
  uint16_t number = (uint16_t)buf[0] | ((uint16_t)buf[1] << 8);

/*
  uint32_t value = 0;
  for (int i = 0; i < len && i < 4; i++) {
    value |= (buf[i] << ((3 - i) * 8));
  }
  */

  /*
  char command[100];
  sprintf(command, "python3 main.py -r=cfg -inp=%u > tmp.txt", number);
  system(command);
  */

  char command[100];
  sprintf(command, "python3 main.py -r=cfg -inp=%u", number);
  system(command);

  /*FILE* pf;
  pf = fopen("./tmp/fuzz_data.bin", "wb");
  fwrite(buf, 1, len, pf);
  fclose(pf);
  system("python3  main.py -r=cfg -inp={buf} >> tmp.txt");*/
  // buf -> chislo -> graph
}

/*void have_hang_or_crush(u8* buf, u32 len)
{
  static u32 n_crush=0;
  FILE *pf_crush;
  u8 buff_name[100];
  sprintf(buff_name, "./tmp/Crushes/crush_%d.bin", n_crush);
  n_crush++;
  pf_crush = fopen(buff_name, "wb");
  fwrite(buf, 1, len, pf_crush);
  fclose(pf_crush);
}*/

void get_cover(u8* buf, u32 len)
{
    /*iters_witout_covers++;
    system("sudo python3 get_cover.py NO");
    usleep(1000);*/
    FILE* pf, *pf_log;
    pf = fopen("./tmp.txt", "rb");
    u8 cur_addr_h, cur_addr_l;
    u16 cur_addr;
    u8 prev_addr = 0;
    //if find hang sleep(10); return;
    if ((fscanf(pf, "%c", &cur_addr_h) != EOF) && (fscanf(pf, "%c", &cur_addr_l) != EOF))
    {
        cur_addr = (u16)(cur_addr_h) * 0x100 + cur_addr_l;
        __afl_area_ptr[prev_addr ^ cur_addr]++;
        prev_addr = cur_addr >> 1;
        while ((fscanf(pf, "%c", &cur_addr_h) != EOF) && (fscanf(pf, "%c", &cur_addr_l) != EOF)) //Читают по два байта номера базовых блоков
        {
          cur_addr = (u16)(cur_addr_h) * 0x100 + cur_addr_l;
          __afl_area_ptr[prev_addr ^ cur_addr]++;
          prev_addr = cur_addr >> 1;
        }
    }
    fclose(pf);
}


void check_iters_witout_covers()
{
    if (iters_witout_covers > 30000)
    {
        system("sudo killall -9 ../../afl-fuzz");
    }
}

int main(int argc, char *argv[]) {

  /* This is were the testcase data is written into */
  u8  buf[0x1000];  // this is the maximum size for a test case! set it!
  s32 len;

  /* here you specify the map size you need that you are reporting to
     afl-fuzz.  Any value is fine as long as it can be divided by 32. */
  __afl_map_size = 65536;  // default is 65536 Число путей в программе, для флэе, вряд ли сильно больше, предположил, что 2048 (думаю с запасом)

  /* then we initialize the shared memory map and start the forkserver */
  __afl_map_shm();
  __afl_start_forkserver();

  while ((len = __afl_next_testcase(buf, sizeof(buf))) > 0) {

    if (len) {  // the minimum data size you need for the target

      /* here you have to create the magic that feeds the buf/len to the
         target and write the coverage to __afl_area_ptr */
      send_fuzz_data(buf, len); // Преобразовать buf в число и передать сгенерированной программе на вход
      get_cover(buf, len);
      //check_iters_witout_covers();
      // remove this, this is just to make afl-fuzz not complain when run

      /*if (buf[0] == 0xff)
        __afl_area_ptr[1] = 1;
      else
        __afl_area_ptr[2] = 2;*/

    }

    /* report the test case is done and wait for the next */
    __afl_end_testcase();

  }

  return 0;

}

