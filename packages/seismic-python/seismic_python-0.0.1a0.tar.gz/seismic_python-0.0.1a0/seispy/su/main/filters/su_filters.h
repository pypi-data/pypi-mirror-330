#ifndef SUFILTERS_H
#define SUFILTERS_H
#include "segy.h"

void bfhighpass_trace(int zerophase, int npoles, float f3db, segy *tr_in, segy *tr);
void bflowpass_trace(int zerophase, int npoles, float f3db, segy *tr_in, segy *tr);

#endif