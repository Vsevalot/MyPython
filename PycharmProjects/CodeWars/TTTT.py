import matplotlib.pyplot as plt

percentage=[10,15,22]
plt.hist(percentage, color='r')
plt.title("Percentage of use mat files for the each group")
plt.xlabel("Group (column)")
plt.ylabel("Percentage")
#plt.axis([0.5, 4.5, 0, 100])
plt.show()