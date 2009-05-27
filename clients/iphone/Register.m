#import "Register.h"

@implementation Register
@synthesize userName;
@synthesize email;
@synthesize firstName;
@synthesize lastName;
@synthesize password;
@synthesize confirmPassword;

CGFloat animatedDistance;
static const CGFloat KEYBOARD_ANIMATION_DURATION = 0.3;
static const CGFloat MINIMUM_SCROLL_FRACTION = 0.2;
static const CGFloat MAXIMUM_SCROLL_FRACTION = 0.8;
static const CGFloat PORTRAIT_KEYBOARD_HEIGHT = 216;
static const CGFloat LANDSCAPE_KEYBOARD_HEIGHT = 162;


- (IBAction)sendRegistrationInfo {
	NSString *post = [NSString stringWithFormat:@"username=%@&email=%@&firstName=%@&lastName=%@&password=%@&confirmPassword=%@",
	 userName.text, email.text, firstName.text, lastName.text, 
	 password.text, confirmPassword.text, 123];
   // NSString *post = @"cool=val1&key2=val2";
	NSLog(post);
    NSData *postData = [post dataUsingEncoding:NSASCIIStringEncoding allowLossyConversion:YES];
	
    NSString *postLength = [NSString stringWithFormat:@"%d", [postData length]];
	
    NSMutableURLRequest *request = [[[NSMutableURLRequest alloc] init] autorelease];
    [request setURL:[NSURL URLWithString:@"http://localhost:8080/callme/test/"]];
    [request setHTTPMethod:@"POST"];
    [request setValue:postLength forHTTPHeaderField:@"Content-Length"];
    [request setValue:@"application/x-www-form-urlencoded" forHTTPHeaderField:@"Content-Type"];
    [request setHTTPBody:postData];
    
    NSURLConnection *conn=[[NSURLConnection alloc] initWithRequest:request delegate:self];
    if (conn) 
    {
		NSLog(@"if conn returned true");
        receivedData = [[NSMutableData data] retain];
    } 
    else 
    {
		NSLog(@"if conn returned False. Could not make connection");

        // inform the user that the download could not be made
    }
}

- (void)touchesBegan:(NSSet *)touches withEvent:(UIEvent *)event
{
    // Dismiss the keyboard when the view outside the text field is touched.
	//Going through each text box may not be the best way to do this.
	[userName resignFirstResponder];
	[email resignFirstResponder];
	[firstName resignFirstResponder];
	[lastName resignFirstResponder];
	[password resignFirstResponder];
	[confirmPassword resignFirstResponder];
    // Revert the text field to the previous value.
	// textField.text = self.string; 
	[super touchesBegan:touches withEvent:event];
}

- (void)updateStrings{
	NSLog(userName.text);
	NSLog(email.text);
	NSLog(firstName.text);
	NSLog(lastName.text);
	NSLog(password.text);
	NSLog(confirmPassword.text);
}

- (BOOL)textFieldShouldClear:(UITextField *)textField {
	return NO;
}

- (void)textFieldDidEndEditing:(UITextField *)textField
{
    CGRect viewFrame = self.frame;
    viewFrame.origin.y += animatedDistance;
    
    [UIView beginAnimations:nil context:NULL];
    [UIView setAnimationBeginsFromCurrentState:YES];
    [UIView setAnimationDuration:KEYBOARD_ANIMATION_DURATION];
    
    [self setFrame:viewFrame];
    
    [UIView commitAnimations];
}

- (BOOL) textFieldShouldBeginEditing:(UITextField *)textField{
	{
		CGRect textFieldRect =
        [self.window convertRect:textField.bounds fromView:textField];
		CGRect viewRect =
        [self.window convertRect:self.bounds fromView:self];

		CGFloat midline = textFieldRect.origin.y + 0.5 * textFieldRect.size.height;
		CGFloat numerator =
        midline - viewRect.origin.y
		- MINIMUM_SCROLL_FRACTION * viewRect.size.height;
		CGFloat denominator =
        (MAXIMUM_SCROLL_FRACTION - MINIMUM_SCROLL_FRACTION)
		* viewRect.size.height;
		CGFloat heightFraction = numerator / denominator;
		
		if (heightFraction < 0.0)
		{
			heightFraction = 0.0;
		}
		else if (heightFraction > 1.0)
		{
			heightFraction = 1.0;
		}
		
		animatedDistance = floor(PORTRAIT_KEYBOARD_HEIGHT * heightFraction);
		
		CGRect viewFrame = self.frame;
		viewFrame.origin.y -= animatedDistance;
		
		[UIView beginAnimations:nil context:NULL];
		[UIView setAnimationBeginsFromCurrentState:YES];
		[UIView setAnimationDuration:KEYBOARD_ANIMATION_DURATION];
		
		[self setFrame:viewFrame];
		
		[UIView commitAnimations];
		return YES;
	}
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning]; // Releases the view if it doesn't have a superview.
    // Release anything that's not essential, such as cached data.
}

- (void)connection:(NSURLConnection *)connection didReceiveResponse:(NSURLResponse *)response
{
    [receivedData setLength:0];
}

- (void)connection:(NSURLConnection *)connection didReceiveData:(NSData *)data
{
    [receivedData appendData:data];
}

- (void)connectionDidFinishLoading:(NSURLConnection *)connection
{
    // do something with the data
    // receivedData is declared as a method instance elsewhere
    NSLog(@"Succeeded! Received %d bytes of data",[receivedData length]);
    NSString *aStr = [[NSString alloc] initWithData:receivedData encoding:NSASCIIStringEncoding];
    NSLog(aStr);
	
    // release the connection, and the data object
    [receivedData release];
}


@end
