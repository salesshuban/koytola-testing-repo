server {
    listen [::]:80;
    listen 80;

    server_name koytola.com www.koytola.com;

    # redirect http to https www
    return 301 https://koytola.com$request_uri;
}

server {
    listen [::]:443 ssl http2;
    listen 443 ssl http2;

    server_name www.koytola.com;

    ssl_certificate /etc/letsencrypt/live/koytola.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/koytola.com/privkey.pem;

    root /home/olcaey/koytola/;

    # redirect https non-www to https www
    return 301 https://koytola.com$request_uri;
}

server {
    listen [::]:443 ssl http2;
    listen 443 ssl http2;

    server_name koytola.com;

    root /home/olcaey/koytola/;
    index templates/index.html;
    try_files $uri $uri templates/index.html;
    error_page 404 = @myownredirect;
    error_page 500 = @myownredirect;

    ssl_certificate /etc/letsencrypt/live/koytola.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/koytola.com/privkey.pem;

    location @myownredirect {
        return 302 /;
    }

    location /static/ {
        root /home/olcaey/koytola/;
        access_log off;
        expires 30d;
        add_header Cache-Control "public";
    }

    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_headers_hash_max_size 512;
        proxy_headers_hash_bucket_size 128;

        add_header Content-Security-Policy "img-src * 'self' data: blob: https:; default-src 'self' https://*.googleapis.com https://*.googletagmanager.com https://*.google-analytics.com https://s.ytimg.com https://www.youtube.com https://*.koytola.com https://*.googleapis.com https://*.gstatic.com https://*.w.org https://*.fontawesome.com https://*.amazonaws.com https://*.list-manage.com data: 'unsafe-inline' 'unsafe-eval';" always;
add_header X-Xss-Protection "1; mode=block" always;
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header Referrer-Policy "origin-when-cross-origin" always;
        add_header Strict-Transport-Security "max-age=31536000; includeSubdomains; preload";
    }

}


server {
    listen [::]:443 ssl http2;
    listen 443 ssl http2;

    server_name panel.koytola.com;

    ssl_certificate /etc/letsencrypt/live/koytola.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/koytola.com/privkey.pem;

    location = /favicon.ico {
        access_log off;
        log_not_found off;
    }

    location / {
        root /home/olcaey/koytola/dashboard/build/dashboard/;
        index index.html;
    }

}


server {
    listen [::]:443 ssl http2;
    listen 443 ssl http2;

    server_name api.koytola.com;

    ssl_certificate /etc/letsencrypt/live/koytola.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/koytola.com/privkey.pem;

    location /static/ {
        root /home/olcaey/koytola/;
    }

    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
        proxy_headers_hash_max_size 512;
        proxy_headers_hash_bucket_size 128;

        add_header Content-Security-Policy "img-src * 'self' data: blob: https:; default-src 'self' https://*.koytola.com data: 'unsafe-inline' 'unsafe-eval'; script-src 'self' https://*.koytola.com 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline' 'unsafe-eval'; " always; add_header X-Xss-Protection "1; mode=block" always;
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header Referrer-Policy "origin-when-cross-origin" always;
        add_header Strict-Transport-Security "max-age=31536000; includeSubdomains; preload";
    }

}

server {
    server_name 34.94.143.68;
    return 301 https://koytola.com$request_uri;
}
