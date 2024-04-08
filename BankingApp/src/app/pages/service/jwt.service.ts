import { Injectable } from '@angular/core';
import { jwtDecode } from 'jwt-decode';

@Injectable({
  providedIn: 'root'
})
export class JwtService {

  constructor() { }

  // Store JWT token in local storage
  storeToken(token: string): void {
    localStorage.setItem('token', token);
  }

  // Retrieve JWT token from local storage
  getToken(): string | null {
    return localStorage.getItem('token');
  }

  // Remove JWT token from local storage
  removeToken(): void {
    localStorage.removeItem('token');
  }

  // Decode JWT token
  decodeToken(token: string): any {
    return jwtDecode(token);
  }
}