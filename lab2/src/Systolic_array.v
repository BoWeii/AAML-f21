`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 12/01/2021 02:23:23 PM
// Design Name: 
// Module Name: Systolic_array
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////
`define ARRAY_SIZE 16
`define CHANNEL 4
`define INPUT_SIZE 16
`define KERNEL_SIZE 2

`include "PE.v"

module Systolic_array(clk,reset_n,enable,weight_i,input_i,result_o);
input clk,reset_n,enable;
input [8*`ARRAY_SIZE*`ARRAY_SIZE-1:0] weight_i;
input [8*`ARRAY_SIZE-1:0] input_i;
output [16*`ARRAY_SIZE-1:0] result_o;

wire[15:0] up_w[0:`ARRAY_SIZE-1][0:`ARRAY_SIZE-1];
wire[15:0] down_w[0:`ARRAY_SIZE-1][0:`ARRAY_SIZE-1];
wire[7:0] left_w[0:`ARRAY_SIZE-1][0:`ARRAY_SIZE-1];
wire[7:0] right_w[0:`ARRAY_SIZE-1][0:`ARRAY_SIZE-1];

genvar i,j;
generate
for (i = 0; i < 16; i = i + 1) begin
    assign left_w[i][0] = input_i[ i*8 + 7 : i*8];
end
endgenerate

generate
for (i = 0; i < 16; i = i + 1) begin
    assign up_w[0][i] = 16'b0;
end
endgenerate

generate
for (i = 0; i < 16; i = i + 1) begin
    assign result_o[i * 16 + 15 : i * 16] = down_w[15][i];
end
endgenerate

generate
for (i = 0; i < 16; i = i + 1) begin
    for (j = 0; j < 16; j = j + 1) begin
        PE pe(
            .clk(clk),
            .reset_n(reset_n),
            .enable(enable),
            .down_o(down_w[i][j]),
            .right_o(right_w[i][j]),
            .left_i(left_w[i][j]),
            .weight(weight_i[(i * 16 + j) * 8 + 7 : (i * 16 + j) * 8]),
            .up_i(up_w[i][j])
        );
        
        if (i > 0) begin
            assign up_w[i][j] = down_w[i - 1][j];
        end
        
        if (j > 0) begin
            assign left_w[i][j] = right_w[i][j - 1];
        end
    end
end
endgenerate

endmodule
