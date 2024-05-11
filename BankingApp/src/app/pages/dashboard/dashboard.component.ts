import { Component, OnInit } from '@angular/core';
import { AccountService } from '../../service/acc.service'
import { CommonModule } from '@angular/common';
import { AuthService } from '../../service/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-dashboard',

  standalone: true,
  imports: [ CommonModule ],

  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})

export class DashboardComponent implements OnInit {
  accounts: Account[] = [];

  constructor(private authService: AuthService, private accountService: AccountService, private router: Router) { }

  ngOnInit(): void {
    if (!this.authService.isLoggedIn()) {
      this.router.navigate(['/login']); // Redirect to login if not logged in
    }
    console.log(this.authService.isLoggedIn());
    this.loadAccounts();
  }

  loadAccounts() {
    this.accountService.getMyAccounts().subscribe(
      (response: string) => {
        const jsonResponse = JSON.parse(response); // Parse the JSON string
        this.accounts = jsonResponse as Account[]; // Map the parsed data into the accounts array
        console.log(this.accounts);
      },
      (error) => {
        console.error('Error fetching accounts:', error);
      }
    );
  }

  onLogout(){
    this.authService.logout(); // Call the logout method in your AuthService
    this.router.navigate(['/login']); // Redirect to the login page
  }
}

export interface Account {
  AccountNumber: number,
  AccountType: string,
  Balance: number
}