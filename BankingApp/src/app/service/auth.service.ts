import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, tap } from 'rxjs';
import { JwtService } from './jwt.service';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

    private apiUrl = 'http://127.0.0.1:5000';

    constructor(private http: HttpClient, private jwtService: JwtService) { }
  
    login(username: string, password: string): Observable<any> {
        return this.http.post<any>(`${this.apiUrl}/login`, { Username: username, PasswordHash: password }).pipe(
          tap(response=> {
            this.jwtService.storeToken(response.access_token);
          })
        );
    }
  
    logout(): void {
      this.jwtService.removeToken(); // Remove token from localStorage
    }
  
    isLoggedIn(): boolean {
      return !!this.jwtService.getToken(); // Check if token exists in localStorage
    }

    getToken(): string | null {
      return this.jwtService.getToken();
    }
}