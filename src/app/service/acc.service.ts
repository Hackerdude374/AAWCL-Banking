import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { JwtService } from './jwt.service';

@Injectable({
  providedIn: 'root'
})
export class AccountService {

  private apiUrl = 'http://127.0.0.1:5000';

  constructor(private http: HttpClient, private jwtService : JwtService) { }

  openAccount(accountType: string): Observable<any> {
    const token = this.jwtService.getToken()
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    return this.http.post<any>(`${this.apiUrl}/openaccount`, { AccountType: accountType }, { headers }).pipe(
      catchError((error: any) => {
        console.error('Error opening account:', error);
        return throwError('Error opening account');
      })
    );
  }

  getMyAccounts(): Observable<any> {
    const token = this.jwtService.getToken()
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    return this.http.get<any>(`${this.apiUrl}/myaccounts`, { headers }).pipe(
      catchError((error: any) => {
        console.error('Error fetching accounts:', error);
        return throwError('Error fetching accounts');
      })
    );
  }

  makeTransaction(senderAccountNumber: number, recipientAccountNumber: number, amount: number): Observable<any> {
    const token = this.jwtService.getToken()
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    const data = { sender_account_number: senderAccountNumber, recipient_account_number: recipientAccountNumber, amount };
    return this.http.post<any>(`${this.apiUrl}/transactions`, data, { headers }).pipe(
      catchError((error: any) => {
        console.error('Error making transaction:', error);
        return throwError('Error making transaction');
      })
    );
  }

  showLog(account_number: number): Observable<any> {
    const token = this.jwtService.getToken()
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    const data = { account_number }
    return this.http.post<any>(`${this.apiUrl}/logs`, data, { headers }).pipe(
      catchError((error: any) => {
        console.error('Error fetching accounts:', error);
        return throwError('Error fetching accounts');
      })
    );
  }
}