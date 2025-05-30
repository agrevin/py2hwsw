// SPDX-FileCopyrightText: 2025 IObundle
//
// SPDX-License-Identifier: MIT

`timescale 1 ns / 1 ps

module iob_regarray_sp #(
   parameter ADDR_W = 2,
   parameter DATA_W = 21
) (
   `include "iob_regarray_sp_iob_clk_s_port.vs"
   input rst_i,

   input               we_i,
   input  [ADDR_W-1:0] addr_i,
   input  [DATA_W-1:0] d_i,
   output [DATA_W-1:0] d_o
);

   wire [DATA_W*(2**ADDR_W)-1:0] data_in;
   assign data_in = d_i << (addr_i * DATA_W);
   wire [DATA_W*(2**ADDR_W)-1:0] data_out;
   assign d_o = data_out >> (addr_i * DATA_W);

   genvar i;
   generate
      for (i = 0; i < 2 ** ADDR_W; i = i + 1) begin : g_regarray
         wire reg_en_i;
         assign reg_en_i = we_i & (addr_i == i);
         iob_reg_care #(
            .DATA_W(DATA_W)
         ) regarray_sp_inst (
            `include "iob_regarray_sp_iob_clk_s_s_portmap.vs"
            .rst_i (rst_i),
            .en_i  (reg_en_i),
            .data_i(data_in[DATA_W*(i+1)-1:DATA_W*i]),
            .data_o(data_out[DATA_W*(i+1)-1:DATA_W*i])
         );
      end
   endgenerate

endmodule
