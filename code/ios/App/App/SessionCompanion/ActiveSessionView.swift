import SwiftUI

struct ActiveSessionView: View {
    @State var selectedSession: ActiveSession? = nil
    
    var body: some View {
        VStack {
            Text("2. Active session")
            Text(selectedSession?.id ?? "No active session")
        }
    }
}

#Preview {
    ActiveSessionView()
}
