import numpy as np
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt

# checkpoints
x = np.array([0,1,2])
# delta in days
y = np.array([115,489,1020])

fit_e = curve_fit(lambda t, a, b, c: a+b*np.exp(c*t), x, y)
fit_l = curve_fit(lambda t, a, b: a+b*t, x, y)
xf = np.linspace(0, 6, num = 600)
yf_e = [fit_e[0][0] + fit_e[0][1] * np.exp(fit_e[0][2]*x_val) for x_val in xf]
yf_l = [fit_l[0][0] + fit_l[0][1]*x_val for x_val in xf]

print('{:.3f} + {:.3f}*e^({:.3f}*x)'.format(fit_e[0][0], fit_e[0][1], fit_e[0][2]))
print('2200: {}'.format(yf_e[300]))
print('{:.3f}+{:.3f}*x'.format(fit_l[0][0], fit_l[0][1]))
print('2200: {}'.format(yf_l[300]))

plt.plot(x, y, 'o', label='data')
plt.plot(xf, yf_e, '--', label='fit exp', alpha=.75)
plt.plot(xf, yf_l, '--', label='fit lin', alpha=.75)
ax = plt.gca()
plt.xticks(np.arange(0, max(xf)+1, 1.0))
ax.set_xticklabels([1900+int(100*x) for x in ax.get_xticks().tolist()])
plt.yticks(np.arange(0, max(yf_e)+1, 365.0))
ax.set_yticklabels(['{:.0f}'.format(y/365) for y in ax.get_yticks().tolist()])
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.xlabel('kanji checkpoint')
plt.ylabel('years since last checkpoint')
plt.legend()
plt.show()
