import { HttpEvent, HttpInterceptor, HttpHandler, HttpRequest } from '@angular/common/http';
import { Observable } from 'rxjs';
  
  export class AuthInterceptor implements HttpInterceptor {
    constructor() {}
    
    // Implemented thanks to help from Edmundo Rodrigues at https://stackoverflow.com/questions/34464108/angular-set-headers-for-every-request
    // and Jason Watmore at https://jasonwatmore.com/post/2019/06/26/angular-8-basic-http-authentication-tutorial-example#basic-auth-interceptor-ts

    /**
     * Adds header information to all http requests
     * @param req http request to add header to
     * @param next passes the new req with header info to HTTP request
     */
    intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
      // Clone the request to add the new header
      const clonedRequest = req.clone({ 
          setHeaders: {
            //'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem("token")
          }
        });
  
      // Pass the cloned request instead of the original request to the next handle
      return next.handle(clonedRequest);
    }
  }