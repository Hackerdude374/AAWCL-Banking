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
        let errorMessage = 'An unknown error occurred';
        if (error.error && error.error.error) {
          errorMessage = error.error.error;
        }
        return throwError(errorMessage);
      })
    );
  }

  getMyAccounts(): Observable<any> {
    const token = this.jwtService.getToken()
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    return this.http.get<any>(`${this.apiUrl}/myaccounts`, { headers }).pipe(
      catchError((error: any) => {
        let errorMessage = 'An unknown error occurred';
        if (error.error && error.error.error) {
          errorMessage = error.error.error;
        }
        return throwError(errorMessage);
      })
    );
  }

  changeStauts(account_number: number, account_status: string|undefined): Observable<any> {
    const token = this.jwtService.getToken()
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    const data = { AccountNumber: account_number, AccountStatus: account_status };
    return this.http.post<any>(`${this.apiUrl}/changestatus`, data, { headers }).pipe(
      catchError((error: any) => {
        let errorMessage = 'An unknown error occurred';
        if (error.error && error.error.error) {
          errorMessage = error.error.error;
        }
        return throwError(errorMessage);
      })
    );
  }

  cardStatus(card_number: string, card_status: string|undefined): Observable<any> {
    const token = this.jwtService.getToken()
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    const data = { CardNumber: card_number, CardStatus: card_status };
    return this.http.post<any>(`${this.apiUrl}/cardstatus`, data, { headers }).pipe(
      catchError((error: any) => {
        let errorMessage = 'An unknown error occurred';
        if (error.error && error.error.error) {
          errorMessage = error.error.error;
        }
        return throwError(errorMessage);
      })
    );
  }

  makeTransaction(senderAccountNumber: number, recipientAccountNumber: number, amount: number): Observable<any> {
    const token = this.jwtService.getToken()
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    const data = { sender_account_number: senderAccountNumber, recipient_account_number: recipientAccountNumber, amount };
    return this.http.post<any>(`${this.apiUrl}/transactions`, data, { headers }).pipe(
      catchError((error: any) => {
        let errorMessage = 'An unknown error occurred';
        if (error.error && error.error.error) {
          errorMessage = error.error.error;
        }
        return throwError(errorMessage);
      })
    );
  }

  showLog(account_number: number): Observable<any> {
    const token = this.jwtService.getToken()
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    const data = { account_number }
    return this.http.post<any>(`${this.apiUrl}/logs`, data, { headers }).pipe(
      catchError((error: any) => {
        let errorMessage = 'An unknown error occurred';
        if (error.error && error.error.error) {
          errorMessage = error.error.error;
        }
        return throwError(errorMessage);
      })
    );
  }

  openCard(cardType: string): Observable<any> {
    const token = this.jwtService.getToken()
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    return this.http.post<any>(`${this.apiUrl}/opencard`, { CardType: cardType }, { headers }).pipe(
      catchError((error: any) => {
        let errorMessage = 'An unknown error occurred';
        if (error.error && error.error.error) {
          errorMessage = error.error.error;
        }
        return throwError(errorMessage);
      })
    );
  }

  getMyCards(): Observable<any> {
    const token = this.jwtService.getToken()
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    return this.http.get<any>(`${this.apiUrl}/mycards`, { headers }).pipe(
      catchError((error: any) => {
        let errorMessage = 'An unknown error occurred';
        if (error.error && error.error.error) {
          errorMessage = error.error.error;
        }
        return throwError(errorMessage);
      })
    );
  }
}