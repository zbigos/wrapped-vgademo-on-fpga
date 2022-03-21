import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, ClockCycles, with_timeout

@cocotb.test()
async def test_start(dut):
    clock = Clock(dut.clk, 25, units="ns") # 40M
    cocotb.fork(clock.start())

    dut.power1.value = 0
    dut.power2.value = 0
    dut.power3.value = 0
    dut.power4.value = 0
    dut.RSTB.value = 0

    await ClockCycles(dut.clk, 8)
    dut.power1.value = 1
    await ClockCycles(dut.clk, 8)
    dut.power2.value = 1
    await ClockCycles(dut.clk, 8)
    dut.power3.value = 1
    await ClockCycles(dut.clk, 8)
    dut.power4.value = 1
    await ClockCycles(dut.clk, 80)
    dut.RSTB.value = 1

    await ClockCycles(dut.clk, 400)

    await RisingEdge(dut.uut.mprj.wrapped_vgademo_on_fpga_5.active)

    dut.mprj_io[10].value = 0
    await ClockCycles(dut.clk, 8)
    dut.mprj_io[10].value = 1
    await ClockCycles(dut.clk, 8)
    
    # fingers crossed that we have just reset the chip
    cycle_depth = 0
    zeros_in_cycle = 0
    ones_in_cycle = 0
    
    last_hsync = 0
    startpass = 2

    vcycle_depth = 0
    vzeros_in_cycle = 0
    vones_in_cycle = 0
    
    last_vsync = 0
    vstartpass = 2
    vframe_ok = 0    

    while True:
        await ClockCycles(dut.clk, 1)

        if last_hsync == 0 and dut.mprj_io[11].value == 1:
            if startpass > 0:
                startpass = startpass - 1
            else:
                assert cycle_depth == 800, f"{cycle_depth}, {zeros_in_cycle}, {ones_in_cycle}"
                assert zeros_in_cycle == 96, f"{cycle_depth}, {zeros_in_cycle}, {ones_in_cycle}"
                assert ones_in_cycle == 704, f"{cycle_depth}, {zeros_in_cycle}, {ones_in_cycle}"

            cycle_depth = 0
            zeros_in_cycle = 0
            ones_in_cycle = 0

        cycle_depth += 1
        if dut.mprj_io[11].value == 1:
            ones_in_cycle += 1
        else:
            zeros_in_cycle += 1
        last_hsync = dut.mprj_io[11].value
        #print(dut.flash_csb.value, dut.flash_clk.value, dut.flash_io0.value, dut.flash_io1.value, list(p.value for p in dut.mprj_io))

        if last_vsync == 0 and dut.mprj_io[12].value == 1:
            if vstartpass > 0:
                vstartpass = vstartpass - 1
            else:
                assert vcycle_depth == 419200, f"{vcycle_depth}, {vzeros_in_cycle}, {vones_in_cycle}"
                assert vzeros_in_cycle == 1600, f"{vcycle_depth}, {vzeros_in_cycle}, {vones_in_cycle}"
                assert vones_in_cycle == 417600, f"{vcycle_depth}, {vzeros_in_cycle}, {vones_in_cycle}"
                vframe_ok += 1
                if vframe_ok == 2:
                    return
            vcycle_depth = 0
            vzeros_in_cycle = 0
            vones_in_cycle = 0

        vcycle_depth += 1
        if dut.mprj_io[12].value == 1:
            vones_in_cycle += 1
        else:
            vzeros_in_cycle += 1
        last_vsync = dut.mprj_io[12].value
