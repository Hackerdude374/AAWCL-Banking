import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class SignupService {

    private apiUrl = 'http://127.0.0.1:5000';
  
    constructor(private http: HttpClient) { }
  
    signup(username: string, password: string, email:string, name: string, address:string,phone:string): Observable<any> {
      return this.http.post<any>(`${this.apiUrl}/signup`, { Username: username, PasswordHash: password, Email: email, FullName: name, CurrAddr: address, PhoneNumber: phone});
    }
  }
