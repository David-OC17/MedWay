# Clean the temp files used for analyzing data and creating the .pdf reports
rm dailyReport.aux
rm dailyReport.log
rm dailyReport.out
mv dailyReport.pdf ./reports/dailyReport.pdf

rm ./temp/dailyReport.tex
rm ./temp/temperature_plot.png
rm ./temp/humidity_plot.png
rm ./temp/light_plot.png

rm ./reports/dailyReport.pdf