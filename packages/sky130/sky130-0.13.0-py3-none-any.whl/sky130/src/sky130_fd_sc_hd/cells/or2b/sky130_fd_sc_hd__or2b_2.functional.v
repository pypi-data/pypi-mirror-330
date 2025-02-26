/*
 * Copyright 2020 The SkyWater PDK Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     https://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * SPDX-License-Identifier: Apache-2.0
*/


`ifndef SKY130_FD_SC_HD__OR2B_2_FUNCTIONAL_V
`define SKY130_FD_SC_HD__OR2B_2_FUNCTIONAL_V

/**
 * or2b: 2-input OR, first input inverted.
 *
 * Verilog simulation functional model.
 */

`timescale 1ns / 1ps
`default_nettype none

`celldefine
module sky130_fd_sc_hd__or2b_2 (
    X  ,
    A  ,
    B_N
);

    // Module ports
    output X  ;
    input  A  ;
    input  B_N;

    // Local signals
    wire not0_out ;
    wire or0_out_X;

    //  Name  Output     Other arguments
    not not0 (not0_out , B_N            );
    or  or0  (or0_out_X, not0_out, A    );
    buf buf0 (X        , or0_out_X      );

endmodule
`endcelldefine

`default_nettype wire
`endif  // SKY130_FD_SC_HD__OR2B_2_FUNCTIONAL_V
