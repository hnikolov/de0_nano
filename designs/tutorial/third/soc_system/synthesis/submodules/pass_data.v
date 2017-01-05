module pass_data (
    input reset,
    input clk,
        
    input write,
    input [7:0] writedata,

    output from_hps_write,
    output [7:0] from_hps_writedata
);

assign from_hps_write = write;
assign from_hps_writedata = writedata;


endmodule
