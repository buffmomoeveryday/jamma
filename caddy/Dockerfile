# Use the latest Caddy image
FROM caddy:latest

# Remove the default Caddyfile (optional, Caddy loads configuration from /etc/caddy/Caddyfile by default)
RUN rm /etc/caddy/Caddyfile

# Copy your custom Caddy configuration
COPY Caddyfile /etc/caddy/Caddyfile

# Expose Caddy's default ports for HTTP and HTTPS
EXPOSE 80
EXPOSE 443
