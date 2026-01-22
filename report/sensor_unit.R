# IEEE-style bar plot with mean ± SD error bars + bold title/axis labels
# You can paste this into an R script and run.

install.packages("ggplot2")  # if needed
library(ggplot2)

df <- data.frame(
  distance = factor(c("10 cm", "20 cm", "30 cm"), levels = c("10 cm", "20 cm", "30 cm")),
  mean = c(106.6, 212.2, 308.2),
  sd = c(3.921450979, 1.475729575, 2.097617696)
)

df$label <- sprintf("%.1f \u00B1 %.2f", df$mean, df$sd)

p <- ggplot(df, aes(x = distance, y = mean)) +
  geom_col(width = 0.8) +
  geom_errorbar(
    aes(ymin = mean - sd, ymax = mean + sd),
    width = 0.15,
    linewidth = 0.8
  ) +
  geom_text(
    aes(label = label, y = mean + sd),
    vjust = -0.6,
    fontface = "bold",
    size = 4
  ) +
  labs(
    x = "Testing Distance (Actual)",
    y = "Ultrasonic Sensor Reading (Undetermined Unit)",
    title = "Ultrasonic Sensor Unit Testing (10 trials for each group)"
  ) +
  # Add headroom so the top label never collides with the title
  scale_y_continuous(expand = expansion(mult = c(0, 0.15))) +
  theme_classic(base_size = 12) +
  theme(
    plot.title = element_text(face = "bold", size = 14, hjust = 0.5),
    axis.title.x = element_text(face = "bold", size = 12),
    axis.title.y = element_text(face = "bold", size = 12),
    axis.text.x = element_text(size = 11),
    axis.text.y = element_text(size = 11)
  )

print(p)

# Optional: export in IEEE-friendly formats
# ggsave("ultrasonic_unit_testing.pdf", p, width = 6.5, height = 4.8)
# ggsave("ultrasonic_unit_testing.png", p, width = 6.5, height = 4.8, dpi = 300)

