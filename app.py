from user.user_register import app

if __name__ == '__main__':
    app.run(debug=True)


#postgresql://sign_backend_user:zzlw2WpNJYBhoDpzkWtCdJFRTQcptzqL@dpg-cqe2hv0gph6c73agsk6g-a.oregon-postgres.render.com/sign_backend
#PGPASSWORD=zzlw2WpNJYBhoDpzkWtCdJFRTQcptzqL psql -h dpg-cqe2hv0gph6c73agsk6g-a.oregon-postgres.render.com -U sign_backend_user sign_backend