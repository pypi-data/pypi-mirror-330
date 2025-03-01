#ifndef NCHESS_SRC_NCHESS_H
#define NCHESS_SRC_NCHESS_H

#include "core.h"
#include "board.h"
#include "io.h"
#include "bitboard.h"
#include "types.h"
#include "config.h"
#include "fen.h"
#include "perft.h"
#include "makemove.h"
#include "move.h"
#include "generate.h"

NCH_STATIC void
NCH_Init(){
    NCH_InitTables();
    NCH_InitBitboards();
}

#endif