using FITSIO, Plots


f_strip = FITS("weather_STRIP_ERA5.fits")
f_alma  = FITS("weather_file/weather_ALMA.fits")
f_qubic = FITS("weather_file/weather_QUBIC_3.dits")
f_reijo = FITS("weather_file/weather_Atacama.fits")


seasons_matrix_strip = Array{Float64, 2}(undef, 12, 24)
seasons_matrix_qubic = Array{Float64, 2}(undef, 12, 24)
seasons_matrix_reijo = Array{Float64, 2}(undef, 12, 24)

for i in 2:13
    for j in 1:24
        v = read(f_strip[i], "TQV")[50, j]
        v_q = read(f_qubic[i], "TQV")[50, j]
        v_r = read(f_reijo[i], "TQV")[50, j]
        seasons_matrix_strip[i-1,j] = v #* (1000/997)
        seasons_matrix_qubic[i-1,j] = v_q #* (1000/997)
        seasons_matrix_reijo[i-1,j] = v_r
    end
end

gradient=ColorGradient([:black, :aqua])

heatmap(seasons_matrix_strip, xlabel="Hour", ylabel="Month", zlabel="TQV [mm]", ytick=1:12, xticks=1:24, title = "TQV fluctuations CL 95%", c=gradient, clims=(0,20))

heatmap(seasons_matrix_reijo, xlabel="Hour", ylabel="Month", zlabel="TQV [mm]", ytick=1:12, xticks=1:24, title = "TQV fluctuations CL 50%", c=gradient, clims=(0,9))  

# heatmap(read(f_ten[10], "TQV"))
